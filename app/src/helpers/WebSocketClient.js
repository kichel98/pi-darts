class WebSocketClient {
    constructor(ip='192.168.1.52', port='4321') {
        this.socket = new WebSocket(`ws://${ip}:${port}`)
    }

    setSetterOnMessage(setter) {
        this.socket.onmessage = e => {
            setter(JSON.parse(e.data))
        };
    }
}

export default WebSocketClient;