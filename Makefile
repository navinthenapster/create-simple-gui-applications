all: clean build publish

build:
	asciidoctor -a stylesheet=html.css -a stylesdir=./styles -b html -o build/index.html Book.adoc
	asciidoctor-pdf -o build/book.pdf Book.adoc
	# asciidoctor-epub3 -o build/book.epub Book.adoc

	cp -r ./images ./build/images

publish:
	cp -r ./build/. ~/webapps/martinfitzpatrick_books/create-simple-gui-applications

clean:
	rm -r ./build
 
