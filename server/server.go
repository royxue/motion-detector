package main

import (
    "flag"
    "image"
    "image/png"
    "log"
    "net/http"
    "os"
    "github.com/golang/protobuf/proto"
    "github.com/gorilla/websocket"
    "./msg"
)

var addr = flag.String("addr", "localhost:8080", "http service address")

var upgrader = websocket.Upgrader{}

func handler(w http.ResponseWriter, r *http.Request) {
    c, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Print("upgrade:", err)
        return
    }
    defer c.Close()
    for {
        mt, message, err := c.ReadMessage()
        if err != nil {
            log.Println("read:", err)
            break
        }
        data := &msg.Msg{}
        if err := proto.Unmarshal(message, data); err != nil {
            log.Fatalln("Failed to parse address book:", err)
        }
        log.Printf("receive: %s", data.GetTimestamp())
        err = c.WriteMessage(mt, []byte(data.GetTimestamp()))
        if err != nil {
            log.Println("write:", err)
            break
        }
        // save the image
        rgba_img := image.NewRGBA(image.Rect(0, 0, int(data.GetWidth()), int(data.GetHeight())))
        rgba_img.Pix = data.GetImage()
        file, _ := os.Create("result/" + data.GetCid() + "_" + data.GetTimestamp() + ".png")
        defer file.Close()
        png.Encode(file, rgba_img)
    }
}

func main() {
    flag.Parse()
    log.SetFlags(0)
    http.HandleFunc("/", handler)
    log.Fatal(http.ListenAndServe(*addr, nil))
}
