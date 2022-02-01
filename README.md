# Tema LFA - Sincronizarea automatelor

Tema consta in rezolvarea unor **probleme cu automate deterministe** prin
modelarea lor ca niste **probleme de grafuri**.

Tema este formata din patru task-uri:

1. Gasirea starilor accesibile
2. Gasirea starilor productive
3. Gasirea starilor utile
4. Gasirea unei secvente de sincronizare

## Descrierea task-urilor

1. Gasirea starilor accesibile se face prin pornirea unui **algoritm dfs**
pe graful determinat de automat, dar cu toate starile din care putem pleca
puse in stiva de la inceput. Rezultatul task-ului este lista de noduri
vizitate din cadrul algoritmului dfs.

2. Gasirea starilor productive se face exact ca la primul task, numai
ca trebuie sa rulam dfs-ul pe **graful complementar**.

3. Gasirea starilor utile se face prin rularea celor doua task-uri de mai
sus, iar rezultatul va fi **intersectia nodurilor vizitate ale celor doi
algoritmi**.

4. Gasirea unei secvente de sincronizare se face prin implementarea
algoritmului din paper-ul lui *Sven Sandberg, Homing and Synchronizing
Sequences (Algorithm 2)*. Practic, cat timp secventa de
sincronizare curenta nu sincronizeaza toate nodurile, **aplicam dfs
pe noul graf descris in paper-ul specificat, si adaugam noua secventa
gasita la secventa curenta**. Starile de inceput si starile de final
care pot exista modifica problmea intr-un mod destul de simplist:
daca avem stari de inceput, trebuie sa sincronizam doar starile
de inceput, iar daca avem stari de final, nodul cautat din algoritmul
descris in paper trebuie sa fie printre starile finale.
