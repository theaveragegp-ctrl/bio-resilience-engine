"""
Main entry point for edge node inference service.

Orchestrates video capture, inference pipeline, and cloud communication
for continuous real-time physiological monitoring on NVIDIA Jetson.

Author: Dr. Li Chen
Date: 2024-01-20
"""

import argparse
import logging
import signal
import sys
from typing import Optional
import cv2

from .inference_pipeline import InferencePipeline
from .video_capture import VideoCapture


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EdgeNodeService:
    """Main service class for edge inference node.
    
    Manages the complete edge processing pipeline including video capture,
    inference, and result publishing. Handles graceful shutdown on SIGINT/SIGTERM.
    
    Args:
        model_path: Path to YOLO pose model
        video_source: Video source (camera index, RTSP URL, or video file)
        mqtt_broker: MQTT broker address for cloud communication
        confidence_threshold: Detection confidence threshold
        
    Example:
        >>> service = EdgeNodeService(
        ...     model_path="models/yolov8n-pose.pt",
        ...     video_source=0,
        ...     mqtt_broker="mqtt.bio-resilience.org"
        ... )
        >>> service.run()
    """
    
    def __init__(
        self,
        model_path: str,
        video_source: int | str = 0,
        mqtt_broker: Optional[str] = None,
        confidence_threshold: float = 0.7,
        device: str = "cuda"
    ):
        """Initialize edge node service."""
        self.running = False
        
        # Initialize components
        self.video_capture = VideoCapture(source=video_source)
        self.pipeline = InferencePipeline(
            model_path=model_path,
            confidence_threshold=confidence_threshold,
            device=device,
            mqtt_broker=mqtt_broker
        )
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("EdgeNodeService initialized")
    
    def run(self) -> None:
        """Start the main processing loop.
        
        Continuously captures frames from video source, processes through
        inference pipeline, and publishes results until shutdown signal received.
        """
        pass
    
    def shutdown(self) -> None:
        """Gracefully shutdown the service."""
        pass
    
    def _signal_handler(self, signum: int, frame) -> None:
        """Handle shutdown signals."""
        pass


def main():
    """CLI entry point for edge node service."""
    parser = argparse.ArgumentParser(
        description="Bio-Resilience Engine - Edge Node Service"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="models/yolov8n-pose.pt",
        help="Path to YOLO pose model"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Video source (camera index, RTSP URL, or file path)"
    )
    parser.add_argument(
        "--mqtt-broker",
        type=str,
        default=None,
        help="MQTT broker address (e.g., mqtt.bio-resilience.org)"
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.7,
        help="Detection confidence threshold (0.0-1.0)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "cpu"],
        help="Compute device"
    )
    
    args = parser.parse_args()
    
    # Convert source to int if it's a digit
    source = int(args.source) if args.source.isdigit() else args.source
    
    # Initialize and run service
    service = EdgeNodeService(
        model_path=args.model,
        video_source=source,
        mqtt_broker=args.mqtt_broker,
        confidence_threshold=args.confidence,
        device=args.device
    )
    
    try:
        service.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
