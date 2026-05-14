from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('mock-client/index.html', 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode())
            return
        
        elif self.path == '/players':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            players = json.dumps(["勇士阿强", "法师小明", "游侠小红"])
            self.wfile.write(players.encode())
            return
        
        elif self.path.startswith('/state/'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            state = {
                "roomName": "中央广场",
                "roomDesc": "一个宽敞的广场，中心有一座喷泉",
                "exits": ["north", "south", "east", "west"],
                "players": ["勇士阿强"]
            }
            self.wfile.write(json.dumps(state).encode())
            return
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/command':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            cmd = data.get('command', '')
            
            if cmd == 'look':
                response = "【中央广场】\n一个宽敞的广场，中心有一座喷泉\n出口: north, south, east, west"
            elif cmd == 'go north':
                response = "你向北移动到了【森林小径】\n这里有一条蜿蜒的小路\n出口: south"
            elif cmd == 'who':
                response = "在线玩家: 勇士阿强, 法师小明"
            else:
                response = f"你输入了: {cmd}"
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode())
    
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    port = 4010
    server = HTTPServer(('localhost', port), MockHandler)
    print(f'Mock 服务器运行在 http://localhost:{port}')
    print('访问 http://localhost:4010 开始游戏')
    server.serve_forever()