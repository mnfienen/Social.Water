all: PhotOCR
	g++ PhotOCR.o -o PhotOCR `pkg-config --cflags --libs opencv`
PhotOCR:
	g++ PhotOCR.c -c

clean:
	rm PhotOCR PhotOCR.o
