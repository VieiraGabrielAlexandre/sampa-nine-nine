
"""
Fix para o problema do urllib3.packages.six.moves
"""
import sys
from six.moves import http_client

# Adiciona o módulo http_client ao namespace urllib3.packages.six.moves
sys.modules['urllib3.packages.six.moves.http_client'] = http_client
sys.modules['urllib3.packages.six.moves'] = sys.modules['six.moves']