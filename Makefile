prepare-dist:
	rm -rf dist/ && mkdir dist/
do-dist:
	python gen-dist.py
dist: prepare-dist prepare do-dist
prepare-tests: prepare-dist prepare
prepare:
	cd dist/ && curl 'http://sistemas.anatel.gov.br/areaarea/N_Download/Tela.asp' -H 'Host: sistemas.anatel.gov.br' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://sistemas.anatel.gov.br/areaarea/N_Download/Tela.asp?varMod=Publico&SISQSmodulo=7179' -H 'Cookie: bbbbbbbbbbbbbbb=EAGPKLADAAAAAAAACAGHACAAAAAAAAAAEADAPBEGGDEGAAAADAAAIPLFAPLFAAAA; ASPSESSIONIDQSRCQQCA=LOHLLCDCLLJHCNKDPIPJFICN; BIGipServerpool_sistemas_anatel_pd_asp_areaarea=4076867756.20480.0000; TS012c9f63=01dfc394f0752ef6213ec3c0b562b914f0a451b685d4ac62553ddc0e1c02914edf753bd14daa056cfaa0d8467fecdefeb0b66064a9d864154a32b84cc0862994cdbf206e109ebc806b3ca9038c5a68485e3264aaca86133de349f47fde181ba09652d659fb; BIGipServerpool_sistemas_anatel_pd_asp_sis=3439333548.20480.0000; BIGipServerpool_sistemas_anatel_pd_asp_apoio_sitarweb=1124208812.20480.0000' -H 'Connection: keep-alive' --data 'varTIPO=CentralCNL&varPRESTADORA=&varCENTRAL=F&varUF=&varPERIODO=&acao=c&cmd=&varMOD=Publico' | grep -E -o 'DownLoad/(.*\.ZIP)' | sed 's/DownLoad\///' | awk '{print "wget http://sistemas.anatel.gov.br/AREAAREA/DownLoad/"$$0}' | sh - && unzip *.ZIP && mv *.TXT base.txt
