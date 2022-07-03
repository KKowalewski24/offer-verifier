# Thesis

##### Wymagania 
Dla Windows trzeba miec zainstalowane
* MikTeX
* Python

##### Srodowisko
Aby dobrze działało formatowanie z uzyciem curly brackets {} trzeba uzywac 
IntelliJ 2019.3.5, przy nowszych wersjach dodatek TeXiFy IDEA calkowicie
niszczy formatowanie

##### Development oraz Release
Do developmentu wykorzystywać pierwszy rodzaj ustawień znaków
Do release zakomentować pierwszy rodzaj ustawień znaków i odkomentować 
drugi rodzaj ustawień znaków i budować przy pomocy Overleaf. 
* Pobrać zipa z GitHuba 
* Import project 
* Ustawić rodzaj znaków do release
* Wybrać XeLaTex jako compiler
* Wygenerować pdf, pobrać i sprawdzić czy się tekst dobrze do notatnika kopiuje
```
%----------------------------------%
% Development with local python script (pdflatex)
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[polish]{babel}
\usepackage{polski}
\usepackage{times}

% Release with Overleaf, import zipped project and choose Xelatex as compiler in Overleaf
%\usepackage{fontspec}
%\setmainfont{Times New Roman}
%\usepackage[polish]{babel}
%----------------------------------%
```

##### Struktura 
LATEX może porządkować, numerować i indeksować rozdziały i sekcje dokumentu.
Istnieje 7 poziomów głębokości dla definiowania sekcji w zależności
od klasy dokumentów:
```
    -1	\part{part}
    0	\chapter{chapter}
    1	\section{section}
    2	\subsection{subsection}
    3	\subsubsection{subsubsection}
    4	\paragraph{paragraph}
    5	\subparagraph{subparagraph}
```

##### Obrazki
```
Przykładowy obrazek przedstawia rysunek \ref{example_image}.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,keepaspectratio]{img/example_photo.jpeg}
    \caption[Podpis w spisie rysunków]{Podpis pod rysunkiem}
    \label{example_image}
\end{figure}
```

```
Obrazki obok siebie

\begin{figure}[H]
    \centering
    \begin{minipage}[b]{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth, keepaspectratio]
        {img/example_photo.jpeg}
        \caption
        [Podpis w spisie rysunków]
        {Podpis pod rysunkiem}
        \label{example_image}
    \end{minipage}
    \hfill
    \begin{minipage}[b]{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth, keepaspectratio]
        {img/example_photo.jpeg}
        \caption
        [Podpis w spisie rysunków]
        {Podpis w spisie rysunków}
        \label{example_image}
    \end{minipage}
\end{figure}
```

##### Listingi
```
Przykładowy fragment kodu w tekście: \texttt{console.log('Hello world')}.

Przykładowy listing przedstawia listing \ref{example_listing} - ten sam plik

\begin{code}[H]
\begin{lstlisting}
ReactDOM.render(
  <h1>Hello, world!</h1>,
  document.getElementById('root')
);
\end{lstlisting}
\caption[Podpis w spisie listingów]{Podpis pod listingiem}
\label{example_listing}
\end{code}
```

```
Listingi w odzielnych plikach - należy stworzyc plik w katalogu src/listing

\begin{code}[H]
    \lstinputlisting{../listing/sample.txt}
    \caption[Podpis w spisie listingów]{Podpis pod listingiem}
    \label{example_listing}
\end{code}
```

##### Tabele
[Online table generator](https://www.tablesgenerator.com/)
```
Przykładową tabelę przedstawia tabela \ref{example_table}.
 
\begin{table}[H]
\centering
\begin{tabular}{|c|c|c|c|} 
 \hline
 Kol1 & Kol2 & Kol3 & Kol4 \\ \hline
 1 & 6 & 87837 & 787 \\ \hline
 2 & 7 & 78 & 5415 \\ \hline
 3 & 545 & 778 & 7507 \\ \hline
 4 & 545 & 18744 & 7560 \\ \hline
 5 & 88 & 788 & 6344 \\ \hline
\end{tabular}
\caption[Podpis w spisie tabel]{Podpis nad tabelą}
\label{example_table}
\end{table}
```
##### Bibliografia
Szablon do książki wg polskiej normy
```
@book{book:,
    author = {},
    title = {},
    publisher = {},
    year = {},
    isbn = {}
}
```

Szablon do www wg polskiej normy
```
@misc{website:,
    author = {},
    title = {},
    howpublished = {[online]},
    note = {[dostęp: ]. Dostępny w Internecie, },
    url = {}
}
```

```
Odniesienie do książki \cite{example_book}. 
Odniesienie do strony internetowej \cite{example_website}.
```

##### Pojedyncze znaki 
```
Pierwszy akapit przedstawia tekst, w którym pojedynczy znak 
kończy wiersz, następny akapit przedstawia rozwiązanie tego problemu.

W tekście pracy pojedyncze znaki nie mogą stanowić zakończenia wiersza i kropka. 
Niestety, w tym zdaniu właśnie tak jest.

W tekście pracy pojedyncze znaki nie mogą stanowić zakończenia wiersza i~kropka. 
I jak widać teraz nie znajdują się, wystarczy po pojedynczym znaku zamiast spacji 
użyć tyldy (\~{}).
```
