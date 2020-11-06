## Temat:
*System wspomagający grę w darta poprzez automatyczne naliczanie punktów, oparte na analizie obrazu w czasie rzeczywistym*

## Plan wypowiedzi:
1. **Dart** 
   - opis gry
   - opis tarczy
   - zapotrzebowanie na taki system (bo grają na sizalowych)
2. **Cele**: Umożliwienie wygodnej gry w darta (301 i może inne) bez konieczności ręcznego liczenia punktów.
Dokładniej: 
- wykrycie rzutu i możliwie dokładne ustalenie pozycji wbicia rzutki, a następnie konkretnego pola na tarczy przy ograniczeniach czasowych
- zarządzanie stanem gry w oparciu o jej zasady, odzwierciedlenie logiki
- umożliwienie komunikacji i stworzenie interfejsu, dzięki któremu użytkownik może komunikować się z systemem: odczytywać wyniki i zarządzać stanem gry
- testy dokładności
3. **Koncepcja rozwiązania**:
  
  Komponenty:
   - obraz z kamer jako input
   - RPi 4 + RPi Zero jako kontrolery
   - komunikacja przez sieć z aplikacją mobilną/webową
  
  Do głównego celu (ustalenie trafionego pola) - omówienie rysunku:
   - obliczenia i wykonanie stelaża
   - wykrywanie ruchu (background substraction, absdiff + threshold + kontury)
   - obliczenie kąta pomiędzy środkiem kamery a rzutką/promienia z kamery do rzutki (3 sposoby, interpolacja, ray, ray z kalibracją)
   - triangulacja
   - mapowanie (zamiana na współrzędne biegunowe)



4. **Umiejscowienie**:
   - kompletny "poradnik"
   - mało jest tego typu rozwiązań
   - open source (bo inne zamknięte)
   - niski koszt (bo inne drogie)
   - możliwie ogólne, software możliwy do reużycia dla kogoś innego, duże możliwości konfiguracji
   - dobrze udokumentowane
   - wygląd aplikacji
   - możliwości rozbudowy (nowe gry, statystyki)
   - korekta (gdy system zawiedzie)
   - nie sieć neuronowa, jest kontrola i dobre zrozumienie, możliwość poprawy przy słabych dokładnościach
   - badania dokładności
   - opis algorytmów w pracy, nie tylko używanie czarnych skrzynek
