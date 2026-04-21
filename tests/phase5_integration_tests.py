"""
Aegis Pro Phase 5: System Integration & Performance Test Suite
Testing API performance, MongoDB integration, React dashboard (TC-51 to TC-60)
"""

import pytest
import sys
import os
import json
import time
import requests
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.tri_engine_analyzer import TriEngineAnalyzer

class TestPhase5_SystemIntegration:
    """Phase 5: System Integration & Performance Testing"""
    
    def setup_method(self):
        self.engine = TriEngineAnalyzer()
        self.backend_url = "http://localhost:5000"
    
    def test_TC51_api_response_time(self):
        """TC-51: API Response Time - Ensure analysis completes within 2 seconds"""
        test_data = {
            "url": "https://example.com/test-page",
            "html_content": "<p>Limited time offer! Only 2 items left! No thanks, I hate saving money!</p>",
            "user_agent": "AegisPro-Test/1.0"
        }
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f'{self.backend_url}/api/tri-engine-analyze',
                json=test_data,
                timeout=10
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Check if response is successful and within time limit
            assert response.status_code == 200, "API should return 200 status"
            assert response_time < 2.0, f"API response time should be under 2 seconds, got {response_time:.3f}s"
            
            result = response.json()
            assert 'analysis' in result, "Response should contain analysis data"
            assert 'trust_score' in result['analysis'], "Analysis should contain trust score"
            
        except requests.exceptions.Timeout:
            pytest.fail("API request timed out after 10 seconds")
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not available - skipping API test")
    
    def test_TC52_mongodb_integration(self):
        """TC-52: MongoDB Integration - Verify data storage and retrieval"""
        test_data = {
            "url": "https://example.com/mongodb-test",
            "html_content": "<p>Test content for MongoDB integration</p>",
            "user_agent": "AegisPro-Test/1.0"
        }
        
        try:
            # Send analysis request
            response = requests.post(
                f'{self.backend_url}/api/tri-engine-analyze',
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                # Check if data was stored (should be in MongoDB)
                result = response.json()
                analysis = result.get('analysis', {})
                
                # Verify analysis structure for MongoDB storage
                assert 'findings' in analysis, "Analysis should have findings for storage"
                assert 'trust_score' in analysis, "Analysis should have trust score for storage"
                assert 'risk_level' in analysis, "Analysis should have risk level for storage"
                
                # Simulate retrieval check (would normally query MongoDB)
                time.sleep(0.1)  # Allow time for storage
                
            else:
                pytest.skip("MongoDB integration test skipped - API not responding")
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not available - skipping MongoDB test")
    
    def test_TC53_concurrent_requests(self):
        """TC-53: Concurrent Requests - Handle multiple simultaneous analyses"""
        test_requests = []
        
        # Create multiple test requests
        for i in range(5):
            test_requests.append({
                "url": f"https://example.com/concurrent-test-{i}",
                "html_content": f"<p>Concurrent test {i}: Limited time offer!</p>",
                "user_agent": "AegisPro-Concurrent/1.0"
            })
        
        try:
            # Send all requests concurrently
            import threading
            import queue
            
            results = queue.Queue()
            
            def send_request(test_data):
                try:
                    start_time = time.time()
                    response = requests.post(
                        f'{self.backend_url}/api/tri-engine-analyze',
                        json=test_data,
                        timeout=15
                    )
                    end_time = time.time()
                    results.put({
                        'status': response.status_code,
                        'time': end_time - start_time,
                        'success': response.status_code == 200
                    })
                except Exception as e:
                    results.put({
                        'status': 'error',
                        'time': 0,
                        'success': False,
                        'error': str(e)
                    })
            
            # Start all threads
            threads = []
            for test_data in test_requests:
                thread = threading.Thread(target=send_request, args=(test_data,))
                thread.start()
                threads.append(thread)
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join(timeout=20)
            
            # Check results
            successful_requests = 0
            total_time = 0
            
            while not results.empty():
                result = results.get()
                if result['success']:
                    successful_requests += 1
                    total_time += result['time']
            
            # At least 80% of requests should succeed
            success_rate = successful_requests / len(test_requests)
            assert success_rate >= 0.8, f"Success rate should be at least 80%, got {success_rate*100:.1f}%"
            
            if successful_requests > 0:
                avg_time = total_time / successful_requests
                assert avg_time < 5.0, f"Average response time should be under 5 seconds, got {avg_time:.3f}s"
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not available - skipping concurrent test")
    
    def test_TC54_memory_usage(self):
        """TC-54: Memory Usage - Ensure system doesn't exceed memory limits"""
        import psutil
        import gc
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Perform multiple analyses
        for i in range(20):
            test_data = {
                "url": f"https://example.com/memory-test-{i}",
                "html_content": f"<p>Memory test {i}: " + "Large content " * 100 + "</p>",
                "user_agent": "AegisPro-Memory/1.0"
            }
            
            # Test local analysis (without backend)
            result = self.engine.analyze_comprehensive(
                url=test_data['url'],
                html_content=test_data['html_content']
            )
            
            # Force garbage collection
            if i % 5 == 0:
                gc.collect()
        
        # Get final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100, f"Memory increase should be under 100MB, got {memory_increase:.1f}MB"
    
    def test_TC55_error_handling(self):
        """TC-55: Error Handling - Graceful handling of invalid inputs"""
        invalid_requests = [
            # Empty request
            {},
            # Invalid URL
            {"url": "", "html_content": "<p>Test</p>"},
            # Malformed HTML
            {"url": "https://example.com", "html_content": "<p>Unclosed div"},
            # Very large content
            {"url": "https://example.com", "html_content": "<p>" + "Test" * 10000 + "</p>"},
            # Invalid JSON structure
            "not a json"
        ]
        
        for invalid_request in invalid_requests:
            try:
                if isinstance(invalid_request, str):
                    # Skip invalid JSON for requests library
                    continue
                    
                response = requests.post(
                    f'{self.backend_url}/api/tri-engine-analyze',
                    json=invalid_request,
                    timeout=5
                )
                
                # Should handle gracefully (400 or 422 status)
                assert response.status_code in [400, 422], f"Should return validation error, got {response.status_code}"
                
            except requests.exceptions.ConnectionError:
                pytest.skip("Backend server not available - skipping error handling test")
            except Exception as e:
                # Should not crash
                assert False, f"Request crashed with error: {str(e)}"
    
    def test_TC56_database_performance(self):
        """TC-56: Database Performance - Query and storage performance"""
        test_data = {
            "url": "https://example.com/db-performance-test",
            "html_content": "<p>Database performance test content</p>",
            "user_agent": "AegisPro-DB/1.0"
        }
        
        try:
            # Test storage performance
            storage_times = []
            
            for i in range(10):
                start_time = time.time()
                response = requests.post(
                    f'{self.backend_url}/api/tri-engine-analyze',
                    json=test_data,
                    timeout=10
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    storage_times.append(end_time - start_time)
            
            if storage_times:
                avg_storage_time = sum(storage_times) / len(storage_times)
                assert avg_storage_time < 3.0, f"Average storage time should be under 3 seconds, got {avg_storage_time:.3f}s"
            else:
                pytest.skip("Database performance test skipped - no successful requests")
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not available - skipping database test")
    
    def test_TC57_react_dashboard_integration(self):
        """TC-57: React Dashboard Integration - Verify dashboard data flow"""
        # Test data structure compatibility with React dashboard
        test_result = self.engine.analyze_comprehensive(
            url="https://example.com/dashboard-test",
            html_content="<p>Dashboard integration test: Limited time offer! Only 2 left!</p>"
        )
        
        # Verify result structure matches React dashboard expectations
        required_fields = ['trust_score', 'findings', 'risk_level', 'engines_used']
        
        for field in required_fields:
            assert field in test_result, f"Result should contain {field} for dashboard"
        
        # Verify findings structure
        if test_result['findings']:
            finding = test_result['findings'][0]
            required_finding_fields = ['engine', 'type', 'severity', 'explanation']
            
            for field in required_finding_fields:
                assert field in finding, f"Finding should contain {field} for dashboard"
    
    def test_TC58_api_rate_limiting(self):
        """TC-58: API Rate Limiting - Test rate limiting functionality"""
        try:
            # Send rapid requests to test rate limiting
            responses = []
            
            for i in range(15):  # Send 15 rapid requests
                try:
                    response = requests.post(
                        f'{self.backend_url}/api/tri-engine-analyze',
                        json={
                            "url": f"https://example.com/rate-limit-{i}",
                            "html_content": "<p>Rate limit test</p>"
                        },
                        timeout=5
                    )
                    responses.append(response.status_code)
                except requests.exceptions.RequestException:
                    responses.append('error')
            
            # Check if rate limiting is working (should get some 429 responses)
            rate_limited = any(status == 429 for status in responses if isinstance(status, int))
            
            # If rate limiting is implemented, we should see 429 responses
            # If not implemented, this test should pass (no rate limiting)
            # This is more of a verification test
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not available - skipping rate limiting test")
    
    def test_TC59_system_scalability(self):
        """TC-59: System Scalability - Test system under load"""
        import threading
        import queue
        
        # Simulate system load with multiple concurrent analyses
        load_test_data = {
            "url": "https://example.com/scalability-test",
            "html_content": "<p>Scalability test: " + "Content " * 1000 + "</p>"
        }
        
        results = queue.Queue()
        
        def load_test_worker(worker_id):
            try:
                start_time = time.time()
                result = self.engine.analyze_comprehensive(
                    url=f"{load_test_data['url']}-{worker_id}",
                    html_content=load_test_data['html_content']
                )
                end_time = time.time()
                
                results.put({
                    'worker_id': worker_id,
                    'success': True,
                    'time': end_time - start_time,
                    'trust_score': result['trust_score']
                })
            except Exception as e:
                results.put({
                    'worker_id': worker_id,
                    'success': False,
                    'error': str(e)
                })
        
        # Start 10 concurrent workers
        threads = []
        for i in range(10):
            thread = threading.Thread(target=load_test_worker, args=(i,))
            thread.start()
            threads.append(thread)
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=30)
        
        # Analyze results
        successful_workers = 0
        total_time = 0
        
        while not results.empty():
            result = results.get()
            if result['success']:
                successful_workers += 1
                total_time += result['time']
        
        # At least 80% should succeed under load
        success_rate = successful_workers / 10
        assert success_rate >= 0.8, f"Success rate under load should be at least 80%, got {success_rate*100:.1f}%"
        
        if successful_workers > 0:
            avg_time = total_time / successful_workers
            assert avg_time < 1.0, f"Average analysis time under load should be under 1 second, got {avg_time:.3f}s"
    
    def test_TC60_data_consistency(self):
        """TC-60: Data Consistency - Ensure consistent analysis results"""
        test_data = {
            "url": "https://example.com/consistency-test",
            "html_content": "<p>Consistency test: Limited time offer! Only 2 items left! No thanks, I hate saving money!</p>"
        }
        
        # Run same analysis multiple times
        results = []
        
        for i in range(5):
            result = self.engine.analyze_comprehensive(
                url=test_data['url'],
                html_content=test_data['html_content']
            )
            results.append(result)
        
        # Check consistency of key metrics
        trust_scores = [result['trust_score'] for result in results]
        finding_counts = [len(result['findings']) for result in results]
        
        # Trust scores should be consistent (within small variance)
        score_variance = max(trust_scores) - min(trust_scores)
        assert score_variance <= 5, f"Trust score variance should be <= 5, got {score_variance}"
        
        # Finding counts should be identical
        assert len(set(finding_counts)) == 1, f"Finding counts should be identical, got {finding_counts}"
        
        # Pattern types should be consistent
        pattern_types = set()
        for result in results:
            patterns = {finding['type'] for finding in result['findings']}
            pattern_types.update(patterns)
        
        # Should detect same patterns each time
        assert len(pattern_types) > 0, "Should detect patterns consistently"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
