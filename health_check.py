#!/usr/bin/env python3
"""
Health Check Endpoint

Simple health check endpoint for Docker health checks.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "environment": os.getenv('ENVIRONMENT', 'development'),
                "snowflake_configured": bool(os.getenv('SNOWFLAKE_ACCOUNT')),
                "groq_configured": bool(os.getenv('GROQ_API_KEY'))
            }
            
            self.wfile.write(json.dumps(health_status).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_health_server(port=8000):
    """Run the health check server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print(f"Health check server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_health_server() 