import argparse
import pandas as pd
import logging
from pathlib import Path
import sys
import os

# Setup basic logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Try to import modules
try:
    from scripts.timeline_reconstructor import DiskTimelineAnalyzer
    from scripts.anomaly_detector import AnomalyDetector
    from scripts.visualizer import ForensicVisualizer
    logger.info("Successfully imported all modules")
    
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.info("Trying alternative import method...")
    
    # Alternative import method
    import importlib.util
    
    # Import timeline_reconstructor
    spec = importlib.util.spec_from_file_location("timeline_reconstructor", "scripts/timeline_reconstructor.py")
    timeline_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(timeline_module)
    DiskTimelineAnalyzer = timeline_module.DiskTimelineAnalyzer
    
    # Import anomaly_detector - Check for class name
    spec = importlib.util.spec_from_file_location("anomaly_detector", "scripts/anomaly_detector.py")
    anomaly_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(anomaly_module)
    
    # Check which class exists
    if hasattr(anomaly_module, 'AnomalyDetector'):
        AnomalyDetector = anomaly_module.AnomalyDetector
    elif hasattr(anomaly_module, 'HybridAnomalyDetector'):
        AnomalyDetector = anomaly_module.HybridAnomalyDetector
    else:
        logger.error("No anomaly detector class found in anomaly_detector.py")
        sys.exit(1)
    
    # Import visualizer
    spec = importlib.util.spec_from_file_location("visualizer", "scripts/visualizer.py")
    visualizer_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(visualizer_module)
    ForensicVisualizer = visualizer_module.ForensicVisualizer

def setup_directories():
    """Create required directories"""
    directories = ['data', 'output', 'logs', 'scripts', 'data/raw', 'data/processed']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Disk Forensic Timeline Analyzer')
    parser.add_argument('--evidence_path', default='./data', help='Path to evidence files')
    parser.add_argument('--output_dir', default='./output', help='Output directory')
    parser.add_argument('--no_synthetic', action='store_true', help='Exclude synthetic anomalies')
    
    args = parser.parse_args()
    
    # Setup directories
    setup_directories()
    
    try:
        # Initialize components
        logger.info("Initializing Disk Forensic Analyzer...")
        analyzer = DiskTimelineAnalyzer(args.evidence_path)
        
        # Build timeline
        logger.info("Building timeline from artifacts...")
        timeline = analyzer.build_timeline(include_synthetic=not args.no_synthetic)
        
        if timeline.empty:
            logger.error("No timeline data was generated. Please check data collection.")
            return
        
        # Detect anomalies
        logger.info("Running anomaly detection...")
        detector = AnomalyDetector(timeline)
        anomalies = detector.run_detection()
        
        # Generate visualizations and report
        logger.info("Generating visualizations and report...")
        visualizer = ForensicVisualizer(timeline, anomalies)
        
        # Create output directory
        output_path = Path(args.output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate visualizations (check if methods exist)
        if hasattr(visualizer, 'create_timeline_plot'):
            visualizer.create_timeline_plot()
        
        if hasattr(visualizer, 'create_activity_heatmap'):
            visualizer.create_activity_heatmap()
        
        if hasattr(visualizer, 'create_artifact_distribution'):
            visualizer.create_artifact_distribution()
        
        if hasattr(visualizer, 'generate_report'):
            report = visualizer.generate_report()
        
        # Save results
        timeline.to_csv(output_path / 'timeline.csv', index=False)
        if not anomalies.empty:
            anomalies.to_csv(output_path / 'anomalies.csv', index=False)
        
        logger.info(f"Analysis complete!")
        logger.info(f"- Timeline entries: {len(timeline)}")
        logger.info(f"- Anomalies detected: {len(anomalies)}")
        logger.info(f"- Reports saved to: {args.output_dir}/")
        
        # Print summary to console
        print("\n" + "="*50)
        print("FORENSIC ANALYSIS COMPLETE")
        print("="*50)
        print(f"Timeline Entries: {len(timeline)}")
        print(f"Anomalies Detected: {len(anomalies)}")
        print(f"Output Directory: {args.output_dir}")
        
        if not timeline.empty and 'artifact_type' in timeline.columns:
            artifact_types = timeline['artifact_type'].unique()
            print(f"Artifact Types: {', '.join(artifact_types)}")
        
        print("="*50)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()