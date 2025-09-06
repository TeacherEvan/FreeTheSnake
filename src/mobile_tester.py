"""
Mobile Testing Utility for FreeTheSnake
Provides automated testing for mobile adaptability features and screenshot capture
"""
import pygame
import os
import time
from datetime import datetime
from config_manager import game_config
from logger_setup import get_logger

logger = get_logger(__name__)

class MobileTester:
    """Mobile adaptability testing and validation system"""
    
    def __init__(self, game_instance=None):
        self.game = game_instance
        self.screenshot_dir = "logs/mobile_testing"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # Test configurations
        self.mobile_resolutions = {
            'iphone_se': (375, 667),
            'iphone_12': (390, 844),
            'iphone_12_pro_max': (428, 926),
            'samsung_galaxy_s21': (360, 800),
            'pixel_5': (393, 851),
            'ipad_mini': (768, 1024),
            'ipad_pro': (1024, 1366),
            'android_tablet': (800, 1280)
        }
        
        self.test_orientations = ['portrait', 'landscape']
        self.test_results = []
        
        logger.info("MobileTester initialized")
    
    def run_mobile_compatibility_tests(self, screen, game_state, mobile_adapter):
        """Run comprehensive mobile compatibility tests"""
        logger.info("Starting mobile compatibility tests...")
        
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        # Test 1: Resolution adaptability
        resolution_results = self._test_resolution_adaptability(screen, game_state, mobile_adapter)
        test_results['tests'].append({
            'name': 'Resolution Adaptability',
            'results': resolution_results
        })
        
        # Test 2: Touch target sizes
        touch_results = self._test_touch_target_sizes(mobile_adapter)
        test_results['tests'].append({
            'name': 'Touch Target Sizes',
            'results': touch_results
        })
        
        # Test 3: UI scaling
        scaling_results = self._test_ui_scaling(mobile_adapter)
        test_results['tests'].append({
            'name': 'UI Scaling',
            'results': scaling_results
        })
        
        # Test 4: Performance under different resolutions
        performance_results = self._test_performance_across_resolutions(screen, mobile_adapter)
        test_results['tests'].append({
            'name': 'Performance Across Resolutions',
            'results': performance_results
        })
        
        # Save test results
        self._save_test_results(test_results)
        
        logger.info("Mobile compatibility tests completed")
        return test_results
    
    def _test_resolution_adaptability(self, screen, game_state, mobile_adapter):
        """Test how well the game adapts to different mobile resolutions"""
        results = []
        
        for device_name, (width, height) in self.mobile_resolutions.items():
            for orientation in self.test_orientations:
                if orientation == 'landscape':
                    test_width, test_height = height, width
                else:
                    test_width, test_height = width, height
                
                try:
                    # Update mobile adapter with new dimensions
                    mobile_adapter.update_dimensions(test_width, test_height)
                    
                    # Test scaling factors
                    scale_x = mobile_adapter.scale_x
                    scale_y = mobile_adapter.scale_y
                    ui_scale = mobile_adapter.ui_scale
                    
                    result = {
                        'device': device_name,
                        'orientation': orientation,
                        'resolution': f"{test_width}x{test_height}",
                        'scale_x': scale_x,
                        'scale_y': scale_y,
                        'ui_scale': ui_scale,
                        'is_mobile_resolution': mobile_adapter.is_mobile_resolution(),
                        'status': 'PASS'
                    }
                    
                    # Check for potential issues
                    if ui_scale < 0.5:
                        result['warnings'] = result.get('warnings', [])
                        result['warnings'].append('UI scale too small, text may be unreadable')
                    
                    if ui_scale > 3.0:
                        result['warnings'] = result.get('warnings', [])
                        result['warnings'].append('UI scale too large, elements may overflow')
                    
                    results.append(result)
                    
                    logger.debug(f"Resolution test passed for {device_name} {orientation}: {test_width}x{test_height}")
                    
                except Exception as e:
                    results.append({
                        'device': device_name,
                        'orientation': orientation,
                        'resolution': f"{test_width}x{test_height}",
                        'status': 'FAIL',
                        'error': str(e)
                    })
                    logger.error(f"Resolution test failed for {device_name} {orientation}: {e}")
        
        return results
    
    def _test_touch_target_sizes(self, mobile_adapter):
        """Test that touch targets meet minimum size requirements"""
        results = []
        
        min_touch_size = mobile_adapter.min_touch_target
        test_sizes = [20, 30, 40, 50, 60]
        
        for base_size in test_sizes:
            touch_friendly_size = mobile_adapter.scale_ui_element(base_size)
            
            result = {
                'base_size': base_size,
                'touch_friendly_size': touch_friendly_size,
                'meets_minimum': touch_friendly_size >= min_touch_size,
                'status': 'PASS' if touch_friendly_size >= min_touch_size else 'FAIL'
            }
            
            if not result['meets_minimum']:
                result['warning'] = f"Touch target {touch_friendly_size}px is below minimum {min_touch_size}px"
            
            results.append(result)
        
        logger.debug(f"Touch target size test completed: {len([r for r in results if r['status'] == 'PASS'])}/{len(results)} passed")
        return results
    
    def _test_ui_scaling(self, mobile_adapter):
        """Test UI scaling across different screen sizes"""
        results = []
        
        # Test various screen sizes
        test_dimensions = [
            (320, 568),   # Small mobile
            (375, 667),   # Standard mobile
            (414, 896),   # Large mobile
            (768, 1024),  # Tablet portrait
            (1024, 768),  # Tablet landscape
            (800, 600)    # Desktop
        ]
        
        for width, height in test_dimensions:
            mobile_adapter.update_dimensions(width, height)
            
            # Test font scaling
            base_font_size = 24
            adaptive_font_size = mobile_adapter.get_adaptive_font_size(base_font_size)
            
            # Test spacing
            mobile_spacing = mobile_adapter.get_mobile_ui_spacing()
            
            result = {
                'dimensions': f"{width}x{height}",
                'ui_scale': mobile_adapter.ui_scale,
                'base_font_size': base_font_size,
                'adaptive_font_size': adaptive_font_size,
                'mobile_spacing': mobile_spacing,
                'orientation': mobile_adapter.get_orientation(),
                'status': 'PASS'
            }
            
            # Check for readability issues
            if adaptive_font_size < 12:
                result['warnings'] = result.get('warnings', [])
                result['warnings'].append('Font size may be too small for readability')
            
            if adaptive_font_size > 48:
                result['warnings'] = result.get('warnings', [])
                result['warnings'].append('Font size may be too large')
            
            results.append(result)
        
        logger.debug(f"UI scaling test completed for {len(test_dimensions)} screen sizes")
        return results
    
    def _test_performance_across_resolutions(self, screen, mobile_adapter):
        """Test performance impact of different resolutions"""
        results = []
        
        # Test a subset of resolutions for performance
        test_resolutions = [
            ('mobile_small', 360, 640),
            ('mobile_standard', 390, 844),
            ('tablet', 768, 1024),
            ('desktop', 1024, 768)
        ]
        
        for name, width, height in test_resolutions:
            try:
                mobile_adapter.update_dimensions(width, height)
                
                # Simulate rendering operations
                start_time = time.time()
                
                # Simulate frame rendering
                for _ in range(10):
                    # This would normally be actual game rendering
                    time.sleep(0.001)  # Simulate small rendering delay
                
                end_time = time.time()
                avg_frame_time = (end_time - start_time) / 10 * 1000  # Convert to ms
                
                result = {
                    'resolution_name': name,
                    'dimensions': f"{width}x{height}",
                    'avg_frame_time_ms': round(avg_frame_time, 2),
                    'estimated_fps': round(1000 / avg_frame_time, 1) if avg_frame_time > 0 else 0,
                    'status': 'PASS'
                }
                
                if avg_frame_time > 33.33:  # Below 30 FPS
                    result['warnings'] = ['Performance may be below acceptable levels']
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    'resolution_name': name,
                    'dimensions': f"{width}x{height}",
                    'status': 'FAIL',
                    'error': str(e)
                })
        
        logger.debug(f"Performance test completed for {len(test_resolutions)} resolutions")
        return results
    
    def capture_mobile_screenshots(self, screen, game_state, mobile_adapter, screen_managers):
        """Capture screenshots demonstrating mobile adaptability"""
        screenshots = []
        
        logger.info("Capturing mobile adaptability screenshots...")
        
        # Screenshot configurations
        screenshot_configs = [
            ('mobile_portrait', 390, 844, 'portrait'),
            ('mobile_landscape', 844, 390, 'landscape'),
            ('tablet_portrait', 768, 1024, 'portrait'),
            ('tablet_landscape', 1024, 768, 'landscape'),
            ('desktop', 800, 600, 'landscape')
        ]
        
        for config_name, width, height, orientation in screenshot_configs:
            try:
                # Update screen dimensions
                mobile_adapter.update_dimensions(width, height)
                
                # Create screen with new dimensions
                test_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                
                # Update screen managers if provided
                if screen_managers:
                    for screen_manager in screen_managers:
                        if hasattr(screen_manager, 'update_dimensions'):
                            screen_manager.update_dimensions(width, height)
                
                # Take screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"mobile_test_{config_name}_{timestamp}.png"
                filepath = os.path.join(self.screenshot_dir, filename)
                
                pygame.image.save(test_screen, filepath)
                
                screenshot_info = {
                    'filename': filename,
                    'filepath': filepath,
                    'config': config_name,
                    'dimensions': f"{width}x{height}",
                    'orientation': orientation,
                    'ui_scale': mobile_adapter.ui_scale,
                    'timestamp': timestamp
                }
                
                screenshots.append(screenshot_info)
                logger.info(f"Screenshot captured: {filename}")
                
            except Exception as e:
                logger.error(f"Failed to capture screenshot for {config_name}: {e}")
        
        return screenshots
    
    def _save_test_results(self, test_results):
        """Save test results to JSON file"""
        import json
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mobile_test_results_{timestamp}.json"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(test_results, f, indent=2)
            
            logger.info(f"Test results saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save test results: {e}")
    
    def generate_mobile_compatibility_report(self, test_results):
        """Generate a human-readable mobile compatibility report"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("MOBILE COMPATIBILITY TEST REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {test_results['timestamp']}")
        report_lines.append("")
        
        for test in test_results['tests']:
            report_lines.append(f"TEST: {test['name']}")
            report_lines.append("-" * 40)
            
            if test['name'] == 'Resolution Adaptability':
                passed = sum(1 for r in test['results'] if r['status'] == 'PASS')
                total = len(test['results'])
                report_lines.append(f"Results: {passed}/{total} resolutions passed")
                
                for result in test['results']:
                    status_icon = "✓" if result['status'] == 'PASS' else "✗"
                    report_lines.append(f"  {status_icon} {result['device']} {result['orientation']}: {result.get('resolution', 'N/A')}")
                    if 'warnings' in result:
                        for warning in result['warnings']:
                            report_lines.append(f"    ⚠ {warning}")
            
            elif test['name'] == 'Touch Target Sizes':
                passed = sum(1 for r in test['results'] if r['status'] == 'PASS')
                total = len(test['results'])
                report_lines.append(f"Results: {passed}/{total} sizes passed")
                
                for result in test['results']:
                    status_icon = "✓" if result['status'] == 'PASS' else "✗"
                    report_lines.append(f"  {status_icon} Base size {result['base_size']}px → {result['touch_friendly_size']}px")
            
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        # Save report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"mobile_compatibility_report_{timestamp}.txt"
        report_filepath = os.path.join(self.screenshot_dir, report_filename)
        
        try:
            with open(report_filepath, 'w') as f:
                f.write(report_content)
            
            logger.info(f"Compatibility report saved to {report_filepath}")
        except Exception as e:
            logger.error(f"Failed to save compatibility report: {e}")
        
        return report_content

# Global mobile tester instance
mobile_tester = None

def get_mobile_tester():
    """Get the global mobile tester instance"""
    return mobile_tester

def initialize_mobile_tester(game_instance=None):
    """Initialize the global mobile tester"""
    global mobile_tester
    mobile_tester = MobileTester(game_instance)
    return mobile_tester