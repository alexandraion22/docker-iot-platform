# Tema 3 SPRC - Platforma IoT folosind Microservicii

## Realizarea temei

- Nume : Ion Alexandra Ana-Maria
- Grupa : 341C1
- Timp de lucru : ~ 30 de ore

## Tehnologiile utilizate

- Interfata pentru vizualizarea datelor - `Grafana`
- Baza de date - `InfluxDB`
- Adaptor - `Python`
- Broker de mesaje - `MQTT Broker` (imaginea eclipse-mosquitto)


## Rularea temei

### Pornire stack

Pentru a putea porni tema este necesara doar rularea comenzii:

    ./run.sh

Aceasta va rula comanda de build a adaptorului `docker-compose -f stack.yml build`
si va porni stack-ul prin comanda `docker stack deploy -c stack.yml sprc3`.

Nu am utilizat variabila SPRC_DVP deoarece nu a fost necesara pentru implementarea mea.

### Oprire stack

Pentru a opri stack-ul, se poate rula:

    docker stack rm sprc3

### Testare

Pentru a putea testa tema, poate fi rulata comanda:

    python3 client.py

Script-ul trimite prin mqtt 160 de intrari noi la fiecare minut (pe un interval cu pana la 8 ore inainte pentru a putea observa
graficele in Grafana), conforme cu exemplele din enuntul temei.

Rezultatele pot fi observate cu ajutorul utilitarului Grafana la adresa http://0.0.0.0:80.

## Implementare

### Arbitru

Arbitrul l-am implementat utilizand Python, dat fiind faptul ca eram familiara cu utilizare MQTT cu Python de la laborator.
Arbitrul creeaza un client pentru baza de date si un client ce se aboneaza la toate topicurile de MQTT.

La primirea fiecarui mesaj(functia "_on_message"), arbitrul realizeaza urmatoarele actiuni:
1. Verifica daca topicul are forma `locatie/statie`
2. Verifica daca payload-ul trimis are un timestamp, daca nu, adauga arbitrul timestamp-ul curent
3. Filtreaza elementele din payload si le pasteraza doar pe cele de tip Int/Float
4. Incarca un vector de obiecte JSON (un obiect corespunde unei masuratori) in baza de date, utilizand clientul de InfluxDB

### InfluxDB

Pentru initializare am setat volumul `/docker-entrypoint-initdb.d/init-db.sh` in fisierul `stack.yml`,
dat fiind faptul ca astfel, la pornirea serviciului, se va rula script-ul ce se afla in ./influxdb/init-db.sh, care creeaza
baza de date "iot", utilizata de Grafana si Arbitru, si ii seteaza durata de viata INFINIT.

Am ales imaginea influxdb:1.8 deoarece avea by default autentificarea disabled si e conforma cu cerinta temei.

### Grafana

Pentru a putea initializa dashboard-urile si sursa de date pentru dashboard-urile din Grafana, am utilizat volumul
`/etc/grafana/provisioning`, iar pentru a pastra modificarile facute in interfata grafica am utilizat volumul
`/var/lib/grafana`. (Puteam si doar sa pastrez partea de provisioning si sa realizez binding, dar mereu modificam 
cate ceva in interfata grafica fara sa imi dau seama, asa ca am decis ca datele modificate sa fie retinute in cel de al 
doilea volum, care poate fi sters oricand, dar partea de provisioning se poate modifica doar manual)


## Porturi si acces Grafana si MQTT

- Portul 80 - Grafana - accesibil prin http://0.0.0.0:80
- Portul 1883 - MQTT - accesibil prin 0.0.0.0:1883


## Impartire Networks

Am impartit seviciile in trei retele diferite, conform cerintei:
- `broker_adapter_network` (MQTT Broker si Python Adapter)
- `adapter_influxdb_network` (Python Adapter si InfluxDB)
- `influxdb_grafana_network` (InfluxDb si Grafana)


## Feedback Tema

Tema a fost chiar foarte interesanta (cel mai mult cred ca mi-a placut partea de adrese IP private si adresarea
serviciilor direct dupa nume, a fost foarte interesant). De asemenea mi-a placut si partea de logging +
reprezentaare in Grafana (chiar daca cea din urma a fost cea mai time-consuming, dat fiind faptul ca nu am
gasit o documentatie care sa ma ajute prea mult).


## Referinte

- [InfluxDB - Sursa Imagine oficiala - De ce am folosit 1.8](https://github.com/influxdata/influxdata-docker/blob/43ef33abc06dd88c28c44ae2cd1850cd0aaed9d1/influxdb/1.8/init-influxdb.sh)
- [Mosquitto Conf](https://mosquitto.org/man/mosquitto-conf-5.html)
- [Grafana Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
