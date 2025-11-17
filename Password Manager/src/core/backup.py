import sqlite3
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
from ..data.cloud_sync import CloudSyncManager

class BackupManager:
    def __init__(self, config, db_path: str):
        self.config = config
        self.db_path = Path(db_path)
        self.backup_dir = Path(config.get('database.backup_path'))
        self.backup_dir.mkdir(exist_ok=True)
        
        self.cloud_sync = None
        if config.get('cloud.enable_sync'):
            self.cloud_sync = CloudSyncManager(config)
    
    def create_backup(self, description: str = "Manual backup") -> str:
        """Create a local backup of the database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.db"
        backup_path = self.backup_dir / backup_name
        
        try:
            # Copy database file
            shutil.copy2(self.db_path, backup_path)
            
            # Add metadata
            self._add_backup_metadata(backup_path, description)
            
            # Upload to cloud if enabled
            if self.cloud_sync:
                self.cloud_sync.upload_backup(str(backup_path), description)
            
            print(f"Backup created: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            print(f"Backup failed: {e}")
            raise
    
    def _add_backup_metadata(self, backup_path: Path, description: str):
        """Add metadata to backup database"""
        try:
            conn = sqlite3.connect(backup_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backup_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                INSERT OR REPLACE INTO backup_metadata (key, value)
                VALUES (?, ?)
            ''', ('backup_time', datetime.now().isoformat()))
            
            cursor.execute('''
                INSERT OR REPLACE INTO backup_metadata (key, value)
                VALUES (?, ?)
            ''', ('description', description))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Failed to add backup metadata: {e}")
    
    def list_backups(self) -> List[dict]:
        """List all available backups"""
        backups = []
        
        # Local backups
        for backup_file in self.backup_dir.glob("backup_*.db"):
            backup_info = self._get_backup_info(backup_file)
            backup_info['type'] = 'local'
            backups.append(backup_info)
        
        # Cloud backups
        if self.cloud_sync:
            cloud_backups = self.cloud_sync.list_backups()
            for cloud_backup in cloud_backups:
                cloud_backup['type'] = 'cloud'
                backups.append(cloud_backup)
        
        # Sort by date (newest first)
        backups.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return backups
    
    def _get_backup_info(self, backup_path: Path) -> dict:
        """Get information about a backup file"""
        try:
            # Get file stats
            stat = backup_path.stat()
            file_size = stat.st_size
            
            # Try to get metadata from database
            conn = sqlite3.connect(backup_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM backup_metadata WHERE key = ?', ('backup_time',))
            row = cursor.fetchone()
            backup_time = row[0] if row else backup_path.stem.replace('backup_', '')
            
            cursor.execute('SELECT value FROM backup_metadata WHERE key = ?', ('description',))
            row = cursor.fetchone()
            description = row[0] if row else 'No description'
            
            conn.close()
            
            return {
                'path': str(backup_path),
                'filename': backup_path.name,
                'timestamp': backup_time,
                'description': description,
                'size': file_size,
                'size_formatted': self._format_file_size(file_size)
            }
            
        except Exception as e:
            print(f"Error reading backup info: {e}")
            return {
                'path': str(backup_path),
                'filename': backup_path.name,
                'timestamp': 'Unknown',
                'description': 'Corrupted backup',
                'size': 0,
                'size_formatted': '0 B'
            }
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def restore_backup(self, backup_path: str) -> bool:
        """Restore from a backup"""
        try:
            # Create a backup of current database first
            self.create_backup("Pre-restore backup")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            print(f"Database restored from: {backup_path}")
            return True
            
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """Remove old backups, keeping only the specified number"""
        backups = self.list_backups()
        local_backups = [b for b in backups if b['type'] == 'local']
        
        if len(local_backups) <= keep_count:
            return 0
        
        # Sort by timestamp and remove oldest
        local_backups.sort(key=lambda x: x.get('timestamp', ''))
        removed_count = 0
        
        for backup in local_backups[:-keep_count]:  # Keep the newest ones
            try:
                Path(backup['path']).unlink()
                removed_count += 1
            except Exception as e:
                print(f"Failed to delete backup {backup['path']}: {e}")
        
        print(f"Removed {removed_count} old backups")
        return removed_count
    
    def auto_backup_if_needed(self) -> bool:
        """Create automatic backup if enough time has passed"""
        if not self.config.get('database.auto_backup'):
            return False
        
        backup_interval = timedelta(hours=self.config.get('database.backup_interval_hours', 24))
        latest_backup = self._get_latest_backup_time()
        
        if latest_backup is None or datetime.now() - latest_backup > backup_interval:
            self.create_backup("Automatic backup")
            return True
        
        return False
    
    def _get_latest_backup_time(self) -> Optional[datetime]:
        """Get the timestamp of the latest backup"""
        backups = self.list_backups()
        if not backups:
            return None
        
        latest_backup = max(backups, key=lambda x: x.get('timestamp', ''))
        
        try:
            # Try to parse ISO format
            return datetime.fromisoformat(latest_backup['timestamp'])
        except ValueError:
            try:
                # Try to parse from filename
                timestamp_str = latest_backup['filename'].replace('backup_', '').replace('.db', '')
                return datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            except ValueError:
                return None