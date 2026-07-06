import os
import shutil
import json
from datetime import datetime
from pathlib import Path
import logging

class DataCollector:
    def __init__(self, output_dir="./data"):
        self.output_dir = Path(output_dir)
        self.setup_logging()
        self.setup_directories()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """Create organized directory structure"""
        directories = [
            'raw/prefetch',
            'raw/event_logs', 
            'raw/registry',
            'raw/browser_history',
            'processed',
            'timeline'
        ]
        
        for directory in directories:
            (self.output_dir / directory).mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Created directory structure in {self.output_dir}")
    
    def collect_prefetch(self):
        """Collect Windows Prefetch files"""
        prefetch_source = Path("C:/Windows/Prefetch")
        prefetch_dest = self.output_dir / "raw/prefetch"
        
        if prefetch_source.exists():
            try:
                count = 0
                for pf_file in prefetch_source.glob("*.pf"):
                    try:
                        shutil.copy2(pf_file, prefetch_dest)
                        count += 1
                    except Exception as e:
                        self.logger.warning(f"Could not copy {pf_file}: {e}")
                
                self.logger.info(f"Collected {count} prefetch files")
                return count
            except Exception as e:
                self.logger.error(f"Error collecting prefetch: {e}")
        else:
            self.logger.warning("Prefetch directory not found")
        
        return 0
    
    def collect_event_logs(self):
        """Collect Windows Event Logs"""
        event_sources = [
            "C:/Windows/System32/winevt/Logs",
            "C:/Windows/System32/config"
        ]
        
        event_dest = self.output_dir / "raw/event_logs"
        count = 0
        
        for source_path in event_sources:
            source = Path(source_path)
            if source.exists():
                for log_file in source.glob("*.evtx"):
                    try:
                        shutil.copy2(log_file, event_dest)
                        count += 1
                    except Exception as e:
                        self.logger.warning(f"Could not copy {log_file}: {e}")
        
        self.logger.info(f"Collected {count} event logs")
        return count
    
    def collect_browser_history(self):
        """Collect browser history"""
        import os
        browser_dest = self.output_dir / "raw/browser_history"
        count = 0
        
        # Chrome
        chrome_path = Path(os.path.expanduser("~")) / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default"
        if chrome_path.exists():
            history_file = chrome_path / "History"
            if history_file.exists():
                try:
                    shutil.copy2(history_file, browser_dest / "chrome_history")
                    count += 1
                    self.logger.info("Collected Chrome history")
                except:
                    pass
        
        # Edge
        edge_path = Path(os.path.expanduser("~")) / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default"
        if edge_path.exists():
            history_file = edge_path / "History"
            if history_file.exists():
                try:
                    shutil.copy2(history_file, browser_dest / "edge_history")
                    count += 1
                    self.logger.info("Collected Edge history")
                except:
                    pass
        
        return count
    
    def collect_system_info(self):
        """Collect system information"""
        import platform
        import socket
        
        system_info = {
            "collection_time": datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "username": os.environ.get('USERNAME', 'Unknown'),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
        
        info_path = self.output_dir / "system_info.json"
        with open(info_path, 'w') as f:
            json.dump(system_info, f, indent=2)
        
        self.logger.info("Collected system information")
        return system_info
    
    def collect_all(self):
        """Collect all artifacts"""
        self.logger.info("Starting data collection...")
        
        results = {
            "collection_time": datetime.now().isoformat(),
            "prefetch_files": self.collect_prefetch(),
            "event_logs": self.collect_event_logs(),
            "browser_history": self.collect_browser_history(),
            "system_info": self.collect_system_info()
        }
        
        # Save collection report
        report_path = self.output_dir / "collection_report.json"
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"Data collection complete! Results: {results}")
        return results

if __name__ == "__main__":
    collector = DataCollector("./data")
    collector.collect_all()