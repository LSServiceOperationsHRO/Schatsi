# SCHA.T.S.I
(GERMAN VERSION AT THE BOTTOM OF EACH CHAPTER)

SCHA.T.S.I - An abbreviation for '**SCH**eduling *A*lgorithm for **T**ext **S**each **I**ntelligence'.
This project is located at the Chair of Service Operation at the University of Rostock. As development progresses, the software is intended to accelerate the analysis of scientific papers and publications and to provide the user with an overview of the interrelationships between papers and a prioritization of publications for the user with respect to his self-imposed specifications, even when hundreds of publications are involved.
In addition to the analysis, the results will be provided not only in tabular form, but additionally in a graphical overview to be able to penetrate the relationships between the papers and their authors.
For this purpose, techniques of text analysis, natural language processing (NLP) and machine learning (ML) are used.

Currently, SCHA.T.S.I can be used on Windows and Linux and with Release 1.3 a Beta version for MacOS accessible (No Guarrentee - Feedback is Welcome) :-)

## How to run SCHATSI

### Systemrequirements

For all operating systems, the presence of a up-to-date **Docker** installation is a prerequisite for using the software, since SCHA.T.S.I is provided as a Docker image.
Furthermore, on a Linux system **Docker-Compose** must be installed additionally, as it is not available in the Linux variant of Docker -in contrast to Docker for Windows.

On Docker's website, installers for all common operating systems are available. Docker: https://www.docker.com/get-started

On Linux, the software stores of the respective distribution can also be used.

A guide for the installation under Windows, should there be problems, can be found here.
https://docs.docker.com/desktop/windows/install/

### Running SCHA.T.S.I

After Docker has been installed you will need to download the latest version of our software. You can find it on the right side of this Github page under **RELEASES**. There you will find a .zip folder for your operating system under each release with the tag "latest release".
Download this and unzip the content into a folder of your choice. 

You will receive two files: "docker-compose.yml", "SCHATSI_RUN" and a PDF file with a summary for using the software.

**Important: The included files must be in the same folder for an error-free functioning of the software!**

To start the software you now have to run the "SCHATSI_RUN" file. That was all. No complicated installations, no configuration. Just start it and that's it. (Note: Under some systems it may be necessary to run the "SCHATSI_RUN" with administrator rights, as Docker requires administrator rights under some systems)

A window will open where you navigate to your folder with the PDF files you want to examine. After that, SCHA.T.S.I will do the work for you and put its results in a folder named "output". You will find this folder in the same place on this system where you placed the two unzipped files.


---
SCHA.T.S.I - Eine Abk??rzung f??r '**SCH**eduling *A*lgorithm for **T**ext **S**each **I**ntelligence'
Dieses Projekt ist am Lehrstuhl Service Operation an der Universit??t Rostock angesiedelt. Mit fortschreitendem Entwicklungsstand soll die Software die Analyse von wissenschaftlichen Papern und Ver??ffentlichungen beschleunigen und dem Nutzer selbst bei hunderten Ver??ffentlichen einen ??berblick ??ber die Zusammenh??nge zwischen den Papern und eine Priorisierung der Ver??ffentlichungen f??r den Nutzer hinsichtlich seiner selbstgestellten Vorgaben bereit stellen.
Neben der Analyse sollen die Ergebnisse nicht nur in tabellarischer Form, sondern zus??tzlich in einer grafischen ??bersicht bereitgestellt werden, um die Zusammenh??nge zwischen den Papern und ihren Autoren durchdringen zu k??nnen.
Dazu werden Techniken der Textanalyse, der Verarbeitung nat??rlicher Sprache (NLP) und des Maschinellen Lernens (ML) eingesetzt.

Aktuell kann SCHA.T.S.I auf Windows und Linux genutzt werden, des Weiteren ist eine Beta Version f??r MacOS ab Release 1.3 verf??gbar (Keine Garantien - Feedback erw??nscht) :-) 

## Wie bringe ich SCHA.T.S.I zum laufen?

### Systemvoraussetzungen
F??r alle Betriebssysteme ist das Vorhandensein einer aktuellen **Docker** Installation Vorraussetzung f??r die Nutzung der Software, da SCHA.T.S.I als Docker-Image bereitgestellt wird.
Des Weiteren muss auf einem Linux-System **Docker-Compose** zus??tzlich installiert werden, da es in der Linux-Variante von Docker -im Gegensatz zu Docker f??r Windows- nicht vorhanden ist.

Auf der Website von Docker sind Installer f??r alle g??ngigen Betriebssysteme vorhanden. Docker: https://www.docker.com/get-started

Auf Linux k??nnen zudem die Software-Stores der jeweiligen Distribution genutzt werden.

Eine Anleitung f??r die Installation unter Windows, sollte es Probleme geben finden Sie hier.
https://docs.docker.com/desktop/windows/install/

### Wie starte ich die Software?
Nachdem Docker installiert wurde m??ssen sich die aktuelle Version unserer Software herunterladen. Diese finden Sie auf der rechten Seite dieser Github-Seite unter **RELEASES**. Dort finden sie unter der Ver??ffentlichung mit dem Tag "latest release" jeweils einen .Zip-Ordner f??r ihr Betriebssystem.
Dieses laden Sie herunter und entpacken den Inhalt in einen Ordner ihrer Wahl. 

Sie erhalten zwei Dateien: "docker-compose.yml", "SCHATSI_RUN" und eine PDF-Datei mit einer Zusammenfassung f??r die Nutzung der Software.

**Wichtig: Die enthaltenen Dateien m??ssen sich f??r ein fehlerfreies Funktionieren der Software in einem gemeinsamen Ordner befinden!**

Um die Software zu starten m??ssen Sie nun noch die "SCHATSI_RUN"-Datei starten. Das war alles. Keine umst??ndlichen Installationen, keine Konfiguration. Einfach starten und das wars. (Hinweis: Unter einigen Systemen kann es n??tig sein, die "SCHATSI_RUN" mit Administratorrechten auszuf??hren, da Docker unter einigen Systemen Administratorrechte voraussetzt)

Es ??ffnet sich ein Fenster, in dem Sie zu ihrem Ordner mit den zu untersuchenden PDF-Dateien navigieren. Im Anschluss daran, wird SCHA.T.S.I die Arbeit f??r Sie ??bernehmen und seine Ergebnisse in einem Ordner mit dem Namen "output" ablegen. Diesen finden Sie an dem Ort auf diesem System, an dem Sie die beiden entpackten Dateien abgelegt haben.
