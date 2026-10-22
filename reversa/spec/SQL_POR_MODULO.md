# Acceso a datos y mensajes por módulo

Recuperado de las cadenas de los `.APP` sin ejecutar el programa.

## `apr_pres.APP`

### Sentencias sobre tablas SIGEP (10)

- `SELECT LEFT(gasto,xlev)+REPLI('0',5-xlev) AS gasto, &campo, SUM(asigmn1+asigme1) AS ini, SUM(asigmn2+asigme2+asigmn3+asigme3+asigmn4+asigme4) AS modif FROM s3pre_ga WHERE 1=1 &whereu &wherea &wheref ORDER BY 2,3,4,5,1 GR`
- `SELECT LEFT(recurso,xlev+1)+REPLI('0',5-xlev-1) AS gasto, &campo, SUM(asigmn1+asigme1) AS ini, SUM(asigmn2+asigme2+asigmn3+asigme3+asigmn4+asigme4) AS modif FROM s3pre_re WHERE 1=1 &whereu &wheref ORDER by 2,3,4,5,1 GROU`
- `SELECT XE.FF+"/"+XE.OF+" "+LEFT(S3FF.DES,30)+[/]+LEFT(S3OF.DES,30);`
- `SELECT XE.FF+"/"+XE.OF+" "+oemt(LEFT(S3FF.DES,30))+[/]+oemt(LEFT(S3OF.DES,30));`
- `locate for R_STOP > oRec.P_STOP`
- `locate for R_STOP >= oRec.P_STOP`
- `select apg+" "+des,tipo from s3aproga order by apg into array aap`
- `select dist ff,of from s3PRE_RE into CURSOR XE`
- `select dist ff,of from s3pre_ga into CURSOR XE`
- `select unidad+" "+desc from s3unidad into arra aun order by unidad`

## `bante_co.APP`

### Sentencias sobre tablas SIGEP (7)

- `select s3mode2`
- `SELECT S3MONEDA`
- `SELECT s3mode2`
- `SELECT s3moneda`
- `select s3cambio`
- `select s3codigo`
- `select s3moneda`

## `bante_si.APP`

### Sentencias sobre tablas SIGEP (26)

- `select s3mode2`
- `SELECT s3auxi && seleccionar tabla de Auxiliares`
- `select s3ctas`
- `DELETE IN s3mode2`
- `INSERT INTO s3auxi (unidad,cta,aux,padrea,razon,ciudad,tel1,tel2,ruc,saldo,dbb,hbb,tipo,ff,of,cuenta) ;`
- `LOCATE ALL FOR ALLTRIM(aux)==ALLTRIM(s3mode2.aux)`
- `LOCATE FOR unidad == m.aunidad AND cta==s3mode2.cuenta AND ALLT(aux)==ALLT(m.apadrea0) AND tipo=[A]`
- `LOCATE FOR unidad==m.aunidad AND cta==s3mode2.cuenta AND ALLT(aux)==ALLT(m.aaux0)`
- `SELECT DISTINCT s3relga.GASTO, s3relga.CTA,s3relga.tipo, s3plan_c.DES,aux ;`
- `SELECT S3CTAS.UNIDAD, S3CTAS.CTA, S3CTAS.SALDOD,;`
- `SELECT S3CTAS.UNIDAD, S3CTAS.CTA, SPACE(S3PLAN_C.nivel*3)+S3PLAN_C.des AS des, ;`
- `SELECT S3MSG`
- `SELECT a.ff + '/' + a.of + ' ' + ALLT(b.des) + '/' + ALLT(c.des) AS todo, a.ff, a.of, a.ff + '/' + a.of FROM (_dirDBF+'s3ff_of') a, (_dirDBF+'s3ff') b, (_dirDBF+'s3of') c WHERE a.ff=b.ff AND a.of=c.of &xcond ORDER BY 2,3`
- `SELECT a.ff, a.of, b.des as desff, c.des as desof FROM (_dirDBF+'s3ff_of') a, (_dirDBF+'s3ff') b, (_dirDBF+'s3of') c WHERE a.ff = b.ff AND a.of = c.of &xcond INTO CURSOR _solo`
- `SELECT s3auxi`
- `SELECT s3ctas`
- `SELECT s3ctas && selecccionar CTAS`
- `SELECT s3gastos`
- `SELECT s3mode2`
- `SELECT s3plan_c`
- `SELECT s3pre_ga`
- `SELECT s3recur`
- `locate for aux=s3mode2.aux and cta=s3mode2.cuenta and unidad=m.aunidad`
- `locate for unidad=m.aunidad and cta=s3mode2.cuenta`
- `seek alltrim(m.aunidad)+s3mode2.apertura+s3mode2.gasto`

### Mensajes / textos de la aplicación (1)

- if seek(s3mode2.cuenta)

## `caif.APP`

### Sentencias sobre tablas SIGEP (10)

- `SELECT DISTIN a.*, b.caif FROM _gastos a LEFT OUTER JOIN s5caifgas b ON a.cta==b.cta AND a.gasto=b.gasto AND b.tipo=[P] AND a.apx = b.apx &fempresa INTO CURSOR _gastos`
- `SELECT DISTIN a.*, b.caif FROM _recurso a, s5caifrec b WHERE a.cta==b.cta and a.recurso==b.recurso and b.tipo=[P] &fempresa INTO CURSOR _recurso`
- `SELECT DISTIN a.*, b.caif FROM s3movco a, s5caifrec b WHERE a.cta==b.cta AND !inlist(a.codtr,[23],[24]) AND a.estado=3 AND b.tipo=[F] &ffechas &funidad &fempresa INTO CURSOR _conta`
- `SELECT DISTINCT a.*, b.caif FROM s3movco a, s5caifgas b WHERE a.cta=b.cta AND !INLI(a.codtr,[23],[24]) AND a.estado=3 AND b.tipo=[F] &ffechas &funidad &fempresa INTO CURSOR _conta`
- `SELECT a.*, b.recurso FROM s3movco a, s3movre b WHERE a.unidad==b.unidad and a.cbte==b.cbte and a.linea=b.linea and a.gareco==[R] and a.estado=3 and inlist(a.codtr,[13],[14],[15],[18],[19],[20],[21],[22]) &ffechas &funid`
- `SELECT a.*, get_apx(b.ap) AS apx , b.gasto, b.ff, b.of, b.et FROM s3movco a, s3movga b WHERE a.unidad==b.unidad and a.cbte==b.cbte and a.linea=b.linea and a.gareco==[G] and a.estado=3 and inlist(a.codtr,'07','09','10','1`
- `SELECT caif, des, SUM(monto) AS anterior FROM (_dirdbf+[s3caifsa]) WHERE 1=1 &_xuni GROUP BY 1 INTO CURSOR _mov`
- `SELECT s3unidad`
- `locate for R_STOP > oRec.P_STOP`
- `locate for R_STOP >= oRec.P_STOP`

## `cge.APP`

### Sentencias sobre tablas SIGEP (38)

- `DELETE FROM (_dirdbf+[s3caypc]) WHERE 1=1`
- `DELETE FROM (_dirdbf+[s3cbanco]) WHERE 1=1`
- `DELETE FROM (_dirdbf+[s3cdeuda])`
- `DELETE FROM (_dirdbf+[s3cdocs]) WHERE 1=1`
- `INSERT INTO (_dirdbf+[s3caypc]) ;`
- `INSERT INTO (_dirdbf+[s3cbanco]) ;`
- `INSERT INTO (_dirdbf+[s3cdeuda]) FROM ARRAY anodos`
- `INSERT INTO (_dirdbf+[s3cdocs]) ;`
- `SELECT &campoa "N" AS jcaso, 00000000000.00 AS ini, &dia_0 AS tr, 00000000000.00 AS dea, &dia_1 AS de, 00000000000.00 AS pea, &dia_2 AS pe, 000000.00 AS us,"N" AS dupli FROM s3PRE_RE &whera_ &groupa INTO TABLE &TM`
- `SELECT &campoa "N" AS jcaso, 000000000000.00 AS ini, &dia_0 AS tr, 00000000000.00 AS coa, &dia_1 AS co, 00000000000.00 AS dea, &dia_2 AS de, 00000000000.00 AS paa, &dia_3 AS pa, 00000000000.00 AS usa, &dia_4 AS us, "N" A`
- `SELECT &campog s3gastos.des,s3gastos.tipo, sum_ini AS ini, sum_tr AS tr, sum_coa AS coa, sum_co AS co, sum_dea AS dea, sum_de AS de, sum_paa AS paa, sum_pa AS pa, sum_usa AS usa, sum_us AS us FROM s3gastos,listo0 WHERE s`
- `SELECT &campog s3recur.des,s3recur.tipo, sum_ini AS ini, sum_tr AS tr, sum_dea AS dea, sum_de AS de, sum_pea AS pea, sum_pe AS pe FROM s3recur,listo0 WHERE s3recur.recurso=listo0.recurso INTO TABLE &listo`
- `SELECT &campos MONTH(fecha) AS mes, codtr, unidad AS __uni, " " AS caso, SUM(Hbb+Hbe-Dbb-Dbe) AS x FROM s3movre WHERE estado=3 &debe &fecha_ &where_ AND INLIST(codtr,[25],[28],[29],[30]) &groupo INTO CURSOR qwerty`
- `SELECT &campos MONTH(fecha) AS mes, codtr, unidad AS __uni, " " AS caso, SUM(dbb+dbe-hbb-hbe) AS x FROM s3movga WHERE estado=3 AND INLIST(codtr,[25],[28],[29],[30]) &debe &fecha_ &where_ &hav_y &groupo INTO CURSOR qwerty`
- `SELECT &campos codtr, unidad AS __uni, cbte, dbb, dbe, hbb, hbe FROM s3movRE WHERE estado=3 AND !INLIST(codtr,[25],[28],[29],[30]) &debe &fecha_ &where_ INTO CURSOR qwerty`
- `SELECT &campos codtr, unidad AS __uni, cbte, dbb, dbe, hbb, hbe FROM s3movga WHERE estado=3 AND !INLIST(codtr,[25],[28],[29],[30]) &debe &fecha_ &where_ &hav_y INTO CURSOR qwerty`
- `SELECT &xmesx , IIF(INLIST(s3cbte.CODTR,[28],[30],[29]),[01],s3cbte.CODTR) AS codtr, caso,RECURSO AS GASTO,FF,OF,ET, SUM(DBB) AS DEBE, SUM(DBE) AS DEBEX, SUM(HBB) AS HABER, SUM(HBE) AS HABERX FROM s3MOVRE,s3cbte WHERE s3`
- `SELECT &xmesx , IIF(INLIST(s3cbte.CODTR,[28],[30],[29]),[01],s3cbte.CODTR) AS codtr, caso,ap,GASTO,FF,OF,ET, SUM(DBB) AS DEBE, SUM(DBE) AS DEBEX, SUM(HBB) AS HABER, SUM(HBE) AS HABERX FROM S3MOVGA,s3cbte WHERE s3movga.un`
- `SELECT &xmesx, cta,ff,of,v.codtr,caso, SUM(dbb+dbe)-SUM(hbb+hbe) AS x FROM s3listoco v,s3cbte c WHERE v.estado=3 AND !INLIST(v.codtr,[23],[24]) AND v.unidad=c.unidad AND v.cbte=c.cbte GROUP BY mes,cta,v.codtr,caso INTO C`
- `SELECT &xmesx, cta,ff,of,v.codtr,caso, SUM(hbb+hbe)-SUM(dbb+dbe) AS x FROM s3listoco v,s3cbte c WHERE v.estado=3 AND !INLIST(v.codtr,[23],[24]) AND v.unidad=c.unidad AND v.cbte=c.cbte GROUP BY mes,cta,ff,of,v.codtr,caso `
- `SELECT &xxunidad c2.cta,x from c2,s3relga where s3relga.cta = c2.cta and gasto=[.] into cursor query1_2`
- `SELECT &xxunidad cta,sum(dbb)-sum(hbb) as x from s3movco where !inlist(codtr,'01','02','04','23','24','25',[28],[29],[30]) &fecha_ &where2_ and gareco=[C] and estado=3 group by 1,2 into cursor c2`
- `SELECT &xxunidad cta,sum(dbb)-sum(hbb) as x from s3movco,qw3 where s3movco.unidad = qw3.unidad and s3MOVCO.cbte = qw3.cbte &where2_ group by 1,2 into cursor qw4`
- `SELECT &xxunidad s3fict.gasto,no_pre.cta,s3fict.des, x from no_pre,s3fict where s3fict.cta=no_pre.cta group by 1,2,3 into cursor no_pre2`
- `SELECT &xxunidad s3plan_c.cta,des,sum(tot) as x from previo,s3plan_c where s3plan_c.cta=previo.cta group by 1,2 into cursor no_pre`

## `det_pres.APP`

### Sentencias sobre tablas SIGEP (17)

- `SELECT * FROM s3movco WHERE cta IN (SELECT DISTINCT cta FROM rapx WHERE gasto=xpartida) AND estado=3 &cuni`
- `SELECT DIST apg FROM s3pre_ga WHERE 1=1 &cuni INTO CURSOR rapx`
- `SELECT DIST gasto FROM s3pre_ga WHERE 1=1 &cuni &cap &cff &cof &cet INTO CURSOR rapx`
- `SELECT DIST recurso FROM s3pre_re WHERE 1=1 &cuni &cff &cof &cet INTO CURSOR rapx`
- `SELECT a.codtr,ap,ff,of,et,a.fecha,a.cbte,a.unidad, dbb+dbe AS debe, hbb+hbe AS haber, caso FROM s3MOVGA AS a LEFT JOIN s3cbte AS b ON a.unidad=b.unidad AND a.cbte=b.cbte WHERE a.estado=3 AND gasto==xpartida AND a.fecha<`
- `SELECT a.codtr,ff,of,et,a.fecha,a.cbte,a.unidad, dbb+dbe AS debe, hbb+hbe AS haber, caso FROM s3movre AS a LEFT JOIN s3cbte AS b ON a.unidad = b.unidad AND a.cbte=b.cbte WHERE a.estado=3 AND recurso==xpartida AND a.fecha`
- `SELECT et+[ ]+des FROM s3et WHERE et IN (SELECT DIST et FROM s3pre_ga WHERE 1=1 &cuni &cap &cff &cof) ORDER BY 1 INTO ARRAY aet`
- `SELECT et+[ ]+des FROM s3et WHERE et IN (SELECT DIST et FROM s3pre_re WHERE 1=1 &cuni &cff &cof) ORDER BY 1 INTO ARRAY aet`
- `SELECT ff+[ ]+des FROM s3ff WHERE ff IN (SELECT DIST ff FROM s3pre_ga WHERE 1=1 &cuni &cap) ORDER BY 1 INTO ARRAY aff`
- `SELECT ff+[ ]+des FROM s3ff WHERE ff IN (SELECT DIST ff FROM s3pre_re WHERE 1=1 &cuni) ORDER BY 1 INTO ARRAY aff`
- `SELECT of+[ ]+des FROM s3of WHERE of IN (SELECT DIST of FROM s3pre_ga WHERE 1=1 &cuni &cap &cff) ORDER BY 1 INTO ARRAY aof`
- `SELECT of+[ ]+des FROM s3of WHERE of IN (SELECT DIST of FROM s3pre_re WHERE 1=1 &cuni &cff) ORDER BY 1 INTO ARRAY aof`
- `locate for R_STOP > oRec.P_STOP`
- `locate for R_STOP >= oRec.P_STOP`
- `select apg+iif(tipo=[S],[ ],[ ])+des,tipo from s3aproga ;`
- `select cta,gasto,s3gr_fin.tipo ;`
- `select gasto,finan.cta,finan.tipo,sum(dbb)-sum(hbb) as x from s3ctas,finan where s3ctas.cta=finan.cta &cuni having x#0 OR SUM(DBB)#0 group by 1,2,3 into cursor rapx`

## `gerencia.APP`

### Sentencias sobre tablas SIGEP (21)

- `SELECT &campoa "N" AS jcaso, 00000000000.00 AS ini, &dia_0 AS tr, 00000000000.00 AS dea, &dia_1 AS de, 00000000000.00 AS pea, &dia_2 AS pe, 000000.00 AS us,"N" AS dupli FROM s3PRE_RE &whera_ &groupa INTO TABLE &TM`
- `SELECT &campoa "N" AS jcaso, 000000000000.00 AS ini, &dia_0 AS tr, 00000000000.00 AS coa, &dia_1 AS co, 00000000000.00 AS dea, &dia_2 AS de, 00000000000.00 AS paa, &dia_3 AS pa, 00000000000.00 AS usa, &dia_4 AS us, "N" A`
- `SELECT &campog s3gastos.des,s3gastos.tipo, sum_ini AS ini, sum_tr AS tr, sum_coa AS coa, sum_co AS co, sum_dea AS dea, sum_de AS de, sum_paa AS paa, sum_pa AS pa, sum_usa AS usa, sum_us AS us FROM s3gastos,listo0 WHERE s`
- `SELECT &campog s3recur.des,s3recur.tipo, sum_ini AS ini, sum_tr AS tr, sum_dea AS dea, sum_de AS de, sum_pea AS pea, sum_pe AS pe FROM s3recur,listo0 WHERE s3recur.recurso=listo0.recurso INTO TABLE &listo`
- `SELECT &campos MONTH(fecha) AS mes, codtr, unidad AS __uni, " " AS caso, SUM(Hbb+Hbe-Dbb-Dbe) AS x FROM s3movre WHERE estado=3 &debe &fecha_ &where_ AND INLIST(codtr,[25],[28],[29],[30]) &groupo INTO CURSOR qwerty`
- `SELECT &campos MONTH(fecha) AS mes, codtr, unidad AS __uni, " " AS caso, SUM(dbb+dbe-hbb-hbe) AS x FROM s3movga WHERE estado=3 AND INLIST(codtr,[25],[28],[29],[30]) &debe &fecha_ &where_ &hav_y &groupo INTO CURSOR qwerty`
- `SELECT &campos codtr, unidad AS __uni, cbte, dbb, dbe, hbb, hbe FROM s3movRE WHERE estado=3 AND !INLIST(codtr,[25],[28],[29],[30]) &debe &fecha_ &where_ INTO CURSOR qwerty`
- `SELECT &campos codtr, unidad AS __uni, cbte, dbb, dbe, hbb, hbe FROM s3movga WHERE estado=3 AND !INLIST(codtr,[25],[28],[29],[30]) &debe &fecha_ &where_ &hav_y INTO CURSOR qwerty`
- `SELECT &x_sqlfield SUM(DBB) as DEBE, SUM(DBE) as DEBEX, SUM(HBB) AS HABER,SUM(HBE) AS HABERX from (_dirdbf+[s3movga]) a,(_dirdbf+[s3cbte]) b where a.unidad = b.unidad AND a.cbte = b.cbte AND b.estado = 3 order by &x_sqlg`
- `SELECT &xcampox, SUM(a.ini) AS Inicial, SUM(a.tr) AS Modif, SUM(a.co) AS Compro, SUM(a.de) AS Deven, SUM(a.pa) AS Pagado FROM LISTO a INNER JOIN (_dirdbf+[s3gastos]) b ON a.gasto=b.gasto AND b.tipo=[S] GROUP BY &xcampox `
- `SELECT * FROM s3movco WHERE estado=3 AND unidad+cbte+STR(linea,6,0) NOT IN (SELECT lineaa FROM NoTomarEnCuenta) &fecha_ &where2_ INTO CURSOR s3listoco`
- `SELECT COUNT(*) as ctd FROM (_dirDBF+'s3pre_ga') WHERE &xwhere INTO CURSOR ddcc`
- `SELECT COUNT(*) as ctd FROM (_dirDBF+'s3pre_re') WHERE &xwhere INTO CURSOR ddcc`
- `SELECT a.*, b.caso FROM a0 a, s3cbte b WHERE b.unidad=a.__uni AND a.cbte=b.cbte &casocond INTO CURSOR a0`
- `SELECT a.*,b.caso FROM a0 a, s3cbte b WHERE b.unidad=a.__uni AND a.cbte=b.cbte &casocond INTO CURSOR a0`
- `SELECT s3ff.ff+[/]+s3of.of+" - "+ALLT(s3ff.des)+[ / ]+ALLT(s3of.des);`
- `SELECT unidad, cta, codtr, cbte, unidad AS __uni, IIF(!EMPTY(ff),ff,xff) AS ff, IIF(!EMPTY(of),of,xof) AS of, SUM(hbb+hbe)-SUM(dbb+dbe) AS monto FROM s3listoco WHERE estado=3 AND codtr<>'23' &netea &ffcond &debe &fecha_ `
- `SELECT unidad, cta, codtr, cbte, unidad AS __uni, IIF(!empty(ff),ff,xff) AS ff, IIF(!empty(of),of,xof) AS of, SUM(dbb+dbe)-SUM(hbb+hbe) AS monto FROM s3listoco WHERE estado=3 AND codtr<>[23] &netea &debe &ffcond &fecha_ `
- `locate for R_STOP > oRec.P_STOP`
- `locate for R_STOP >= oRec.P_STOP`
- `select &x_sqlfield SUM(DBB) as DEBE, SUM(DBE) as DEBEX, SUM(HBB) AS HABER, SUM(HBE) AS HABERX from (_dirdbf+[s3movre]) a,(_dirdbf+[s3cbte]) b where b.unidad=a.unidad AND b.cbte =a.cbte AND b.estado=3 order by &x_sqlgroup`

## `impmodif.app`

### Sentencias sobre tablas SIGEP (13)

- `SELECT s3cbte`
- `SELECT s7catproy`
- `SELECT &_ac_[xlevel+1],00000000000.00 as Disponible, SUM(DBb+DBe-HBb-HBE) AS Total_Cbte, SPACE(10) AS OBS FROM s3MOVGA WHERE cbte=nocbte and unidad=munidad GROUP BY &_ac_[xlevel+1] INTO TABLE &jtabla1`
- `SELECT &bcampos, SUM(asigmn1+asigme1+asigmn2+asigme2+asigmn3+asigme3+asigmn4+asigme4+trasmn+trasme-comprmn-comprme) AS Disponible FROM s3pre_ga WHERE unidad=munidad GROUP BY &bcampos INTO CURSOR jx1`
- `SELECT lote, nro_sol FROM mcabemod WHERE entidad=_aet AND estado = .T. AND nro_sol = VAL(SUBSTR(s3cbte.docres,1,5)) AND ;`
- `SELECT nro_sol FROM mcabemod m ,s3cbte b WHERE m.entidad=_aet AND (b.estado =1) AND b.codtr="30" AND b.unidad=_aunidad AND m.nro_sol = VAL(SUBSTR(b.docres,1,5)) AND m.tipo_modif = VAL(SUBSTR(b.docres,9,3)) AND m.estado =`
- `SELECT s3aproga`
- `SELECT s3cambio`
- `SELECT s3movga`
- `SELECT s3movre`
- `SELECT s3pre_ga`
- `SELECT s3pre_re`
- `SELECT s3unidad`

## `impsfpm.app`

### Sentencias sobre tablas SIGEP (18)

- `SELECT s3unidad`
- `insert into s3unidad (unidad, desc, cbte_vali, cbte_borr, saldook, Saldo_p,Saldo_e,uod,tipo_reg,salini) ; && Se adiciona el campo que indica que la UE es automatica`
- `INSERT INTO s3aproga FROM ARRAY xcatpro`
- `SELECT s3aproga`
- `SELECT s3auxi`
- `SELECT s3ctas`
- `SELECT s3pre_ga`
- `SELECT s3pre_re`
- `SELECT s3cbte`
- `SELECT &_ac_[xlevel+1],00000000000.00 as Disponible, SUM(DBb+DBe-HBb-HBE) AS Total_Cbte, SPACE(10) AS OBS FROM s3MOVGA WHERE cbte=nocbte and unidad=munidad GROUP BY &_ac_[xlevel+1] INTO TABLE &jtabla1`
- `SELECT &bcampos, SUM(asigmn1+asigme1+asigmn2+asigme2+asigmn3+asigme3+asigmn4+asigme4+trasmn+trasme-comprmn-comprme) AS Disponible FROM s3pre_ga WHERE unidad=munidad GROUP BY &bcampos INTO CURSOR jx1`
- `SELECT COUNT(1) CANTIDAD FROM S3UNIDAD INTO CURSOR CANT_UNI`
- `SELECT S3CBTE`
- `SELECT c_unidad.unidad,s3ctas.cta,s3ctas.saldod,s3ctas.saldoh,s3ctas.dbb,s3ctas.hbb FROM s3ctas INTO ARRAY array_ctas`
- `SELECT distinct SUBSTR(docres,AT('[',docres)+1,3) resp FROM s3cbte WHERE codtr = '29' AND estado = 1;`
- `SELECT s3cambio`
- `UPDATE s3aproga ;`
- `select unidad,cbte,codtr FROM s3cbte WHERE codtr = '29' AND estado = 1 AND AT(docrespx,docres)>1;`

## `jconta.APP`

### Sentencias sobre tablas SIGEP (4)

- `SELECT s3cheque.unidad,s3cheque.Cbte,s3cheque.cta,s3cheque.aux, s3cheque.Benefi,s3cheque.Cheque,s3cheque.Monto, s3cbte.fecha, IIF(s3cbte.estado=3,[VALIDADO],[BORRADOR]) AS estado FROM s3cheque INNER JOIN s3cbte ON s3cbte`
- `SELECT unidad,cta,aux,razon,padrea,tipo,saldo,dbb,hbb FROM s3auxi WHERE &jcond0 &jcond1 &jcond2 &jcond3 ORDER BY unidad,cta,aux INTO CURSOR xbux`
- `locate for R_STOP > oRec.P_STOP`
- `locate for R_STOP >= oRec.P_STOP`

## `mant.APP`

### Sentencias sobre tablas SIGEP (88)

- `SELECT * FROM (this.alias_ap) WHERE s3aproga.apg = duplicados.apg INTO CURSOR verif`
- `locate for s3plan_c.cta=cta0`
- `locate for s3unidad.unidad=unidad0`
- `insert into s3ctas (unidad, cta, saldod, saldoh, dbb, hbb) ;`
- `insert into s3plan_c (cta, des, nivel, tipo, aux) ;`
- `DELETE IN s3ff_of`
- `SELECT cta,des FROM s3plan_c WHERE tipo='S' and aux='S' INTO ARRAY efe`
- `SELECT s3auxi`
- `SELECT unidad,desc FROM s3unidad INTO ARRAY efe`
- `insert into s3unidad ;`
- `select ff,des from s3ff order by 1 into array efe`
- `select of,des from s3of order by 1 into array efe`
- `Locate for s3plan_c.cta=Vcta`
- `LOCATE FOR s3aproga.apg=Vapg`
- `SELECT s7catproy`
- `SELECT s7ctaban`
- `SELECT s7ctaban &&,'bco_cta'`
- `insert into s3ctas from array ctas`
- `select unidad0 as unidad, s3plan_c.cta, 0 as saldod, 0 as saldoh, ;`
- `DELETE FOR apg=campo IN s3aproga`
- `DELETE FOR unidad=s3unidad.unidad`
- `DELETE IN s3auxi`
- `DELETE IN s3auxi && Elimina la primera coincidencia.`
- `DELETE IN s3cambio`
- `DELETE IN s3plan_c`

## `pr_cbte.APP`

### Sentencias sobre tablas SIGEP (1)

- `SELECT DISTI a.cbte_a,a.linea_a FROM (_dirdbf+[s3link]) a LEFT OUTER JOIN (xcur) b ON a.unidad = b.unidad AND a.cbte_a=b.cbte AND a.linea_a=b.linea WHERE a.unidad = xUni AND a.cbte_b = xCbteB AND &xwhr AND a.linea_b=xLin`

## `rep_pres.APP`

### Sentencias sobre tablas SIGEP (4)

- `SELECT flujo, SUM(monto) AS anterior, descrip FROM (_dirdbf+[s3flujsa]) WHERE 1=1 &_xuni GROUP BY 1 INTO CURSOR _mov`
- `SELECT gasto,recurso, sum(monto)as anterior FROM (_dirdbf+"s3tesosa") WHERE 1=1 &_xuni GROUP BY 1,2 INTO CURSOR _mov`
- `locate for R_STOP > oRec.P_STOP`
- `locate for R_STOP >= oRec.P_STOP`
