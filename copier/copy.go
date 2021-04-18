package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"sync"
	"time"

	"github.com/vbauerster/mpb/v6"
	"github.com/vbauerster/mpb/v6/decor"
)

func addBar(progress *mpb.Progress, size int64, name string, dest string) *mpb.Bar {
	return progress.AddBar(size,
		mpb.PrependDecorators(
			// simple name decorator
			decor.Name(name),
			// decor.DSyncWidth bit enables column width synchronization
			decor.Percentage(decor.WCSyncSpace),

			decor.CountersKibiByte(" | % 4.2f / % 4.2f"),
		),
		mpb.AppendDecorators(
			// decor.EwmaETA(decor.ET_STYLE_GO, 90),
			// decor.Name(" | "),
			// decor.EwmaSpeed(decor.UnitKiB, "% 4.2f", 60),
			decor.Name("-> "+dest),
		),
	)

}

func CopyWithProgressBars(input string, outputs []string) {
	var wg sync.WaitGroup
	p := mpb.New(
		mpb.WithWidth(50),
		mpb.WithRefreshRate(50*time.Millisecond),
	)

	wg.Add(len(outputs))
	for i, destination := range outputs {
		// open the input file
		infile, err := os.Open(input)
		if err != nil {
			log.Fatal(err)
		}
		defer infile.Close()

		// get its size
		fi, err := infile.Stat()
		if err != nil {
			log.Fatal(err)
		}
		size := fi.Size()

		name := fmt.Sprintf("File #%d:", i)
		bar := addBar(p, size, name, destination)

		proxyReader := bar.ProxyReader(infile)
		defer proxyReader.Close()

		// create the target file
		outfile, err := os.Create(destination)
		if err != nil {
			log.Fatal(err)
		}
		defer outfile.Close()

		// concurrently copy the files from infile to outfile
		go func() {
			defer wg.Done()
			// chunked copy from proxyReader, ignoring errors
			for i := size; i != 0; {
				bytes, err := io.CopyN(outfile, proxyReader, 1024*1024*1024)
				outfile.Sync()
				i -= bytes
				if err != nil && err != io.EOF {
					log.Println(bytes, err)
				}
			}
		}()

	}
	wg.Wait()
	p.Wait()
}
