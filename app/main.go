package main

import (
	"fmt"
	"time"
)

func main() {
	for {
		fmt.Println("Hello world in go")

		time.Sleep(time.Second * 1)
	}
}
