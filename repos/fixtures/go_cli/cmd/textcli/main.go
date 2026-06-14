// Command textcli is a tiny CLI over textkit (AgentDelta fixture).
package main

import (
	"fmt"
	"os"

	"textkit"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("usage: textcli <text>")
		return
	}
	fmt.Println(textkit.Reverse(os.Args[1]))
}
