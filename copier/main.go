package main

import (
	"flag"
)

func (i *arrayFlags) String() string {
	return "my string representation"
}

func (i *arrayFlags) Set(value string) error {
	*i = append(*i, value)
	return nil
}

type arrayFlags []string

func main() {
	var outputs arrayFlags
	flag.Var(&outputs, "output", "Some description for this param.")
	input := flag.String("input", "./inputfile", "Some description for this param.")
	flag.Parse()
	CopyWithProgressBars(*input, outputs)
}
