# Quick test to verify all imports work
print("Testing imports...")

try:
    from scripts.timeline_reconstructor import DiskTimelineAnalyzer
    print("✓ timeline_reconstructor imported")
except Exception as e:
    print(f"✗ timeline_reconstructor import failed: {e}")

try:
    from scripts.anomaly_detector import AnomalyDetector
    print("✓ anomaly_detector imported")
except Exception as e:
    print(f"✗ anomaly_detector import failed: {e}")

try:
    from scripts.visualizer import ForensicVisualizer
    print("✓ visualizer imported")
except Exception as e:
    print(f"✗ visualizer import failed: {e}")

print("\nTesting class instantiation...")

try:
    analyzer = DiskTimelineAnalyzer("./data")
    print("✓ DiskTimelineAnalyzer instantiated")
except Exception as e:
    print(f"✗ DiskTimelineAnalyzer instantiation failed: {e}")

print("\nDone!")