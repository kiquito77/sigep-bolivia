# Diccionario de campos

## `catpro` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `ENTIDAD` | C | 4 | 0 |
| `APG` | C | 8 | 0 |
| `DES` | C | 100 | 0 |
| `TIPO` | C | 1 | 0 |
| `SISIN` | C | 13 | 0 |
| `DESSISIN` | C | 60 | 0 |
| `SECTOR` | C | 6 | 0 |
| `TP_GASTO` | N | 1 | 0 |
| `FPS` | C | 2 | 0 |
| `TP_APG` | N | 1 | 0 |
| `DIRADM` | N | 3 | 0 |
| `UE` | N | 3 | 0 |
| `MACRO_DIST` | N | 4 | 0 |
| `DISTRITO` | N | 4 | 0 |
| `JUNTA` | N | 4 | 0 |
| `FUNCION` | C | 4 | 0 |

## `closemes` (1 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `MES` | I | 4 | 0 |
| `DESC` | C | 15 | 0 |

## `ibackup` (1220 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 16 | 0 |
| `FORMULACIO` | C | 1 | 0 |
| `ENTIDAD` | N | 16 | 0 |
| `ORDENADOR_` | N | 16 | 0 |
| `UNIDAD_EJE` | N | 16 | 0 |
| `PROGRAMA` | N | 16 | 0 |
| `PROYECTO` | N | 16 | 0 |
| `ACTIVIDAD` | N | 16 | 0 |
| `OBJETO_DEL` | C | 5 | 0 |
| `FUENTE_DE_` | N | 16 | 0 |
| `ORGANISMO_` | N | 16 | 0 |
| `ENTIDAD_DE` | N | 16 | 0 |
| `IMPORTE` | N | 16 | 0 |
| `CUENTA_FLU` | C | 5 | 0 |
| `TIPO_INVER` | N | 16 | 0 |
| `FINALIDAD_` | C | 6 | 0 |
| `FUNCION_AU` | C | 6 | 0 |
| `SECTOR_ECO` | N | 16 | 0 |
| `SUB_SECTOR` | N | 16 | 0 |
| `ACTIVIDAD_` | N | 16 | 0 |
| `DIST_GASTO` | C | 1 | 0 |
| `API_ESTADO` | C | 15 | 0 |
| `API_TRANSA` | C | 30 | 0 |
| `USU_CRE` | C | 30 | 0 |
| `FEC_CRE` | D | 8 | 0 |
| `USU_MOD` | C | 30 | 0 |
| `FEC_MOD` | D | 8 | 0 |

## `pptgas` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `ENTIDAD` | C | 4 | 0 |
| `UNIDAD` | C | 3 | 0 |
| `AP` | C | 8 | 0 |
| `GASTO` | C | 5 | 0 |
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `ET` | C | 4 | 0 |
| `IMP` | N | 13 | 2 |

## `pptrec` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `ENTIDAD` | C | 4 | 0 |
| `UNIDAD` | C | 3 | 0 |
| `RECURSO` | C | 5 | 0 |
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `ET` | C | 4 | 0 |
| `IMP` | N | 13 | 2 |

## `r_acteco_ent` (250 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECTOR_ECO` | C | 2 | 0 |
| `ENTIDAD` | C | 4 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |

## `r_acteco_finfun` (46 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECTOR_ECO` | C | 2 | 0 |
| `FINALIDAD` | C | 2 | 0 |
| `RELACION` | C | 1 | 0 |

## `r_ei_gasto_ele` (195 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECUENCIAL` | N | 6 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `SECTOR_ECO` | C | 2 | 0 |
| `SUBSEC_ECO` | C | 2 | 0 |
| `ACT_ECO` | C | 2 | 0 |
| `FINALIDAD` | C | 2 | 0 |
| `GRP_FUN` | C | 2 | 0 |
| `FUNCION` | C | 2 | 0 |
| `PROGRAMA` | C | 2 | 0 |
| `PRY_DESDE` | C | 20 | 0 |
| `PRY_HASTA` | C | 20 | 0 |
| `ACT_DESDE` | C | 3 | 0 |
| `ACT_HASTA` | C | 3 | 0 |
| `DES_CATPRG` | C | 110 | 0 |
| `DES_CATPRY` | C | 110 | 0 |
| `TIPO_GASTO` | C | 8 | 0 |

## `r_entidad` (587 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `ENTIDAD` | C | 4 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `DESC_ENT` | C | 100 | 0 |
| `SIG_ENT` | C | 15 | 0 |

## `r_fte_org` (798 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECUENCIA` | N | 8 | 0 |
| `GASTO_REC` | C | 1 | 0 |
| `GRUPO_FTE` | C | 1 | 0 |
| `FUENTE` | C | 2 | 0 |
| `GRUPO_ORG` | C | 1 | 0 |
| `SUBGRP_ORG` | C | 1 | 0 |
| `ORG_FIN` | C | 3 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `ENTIDAD` | C | 4 | 0 |

## `r_fuentes` (22 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `FUENTE` | C | 2 | 0 |
| `GRUPO_FTE` | C | 1 | 0 |
| `DESC` | C | 60 | 0 |
| `SIGLA` | C | 15 | 0 |

## `r_obj_ent` (387 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECUENCIA` | N | 8 | 0 |
| `GRUPO_OBJ` | C | 1 | 0 |
| `SUBGRP_OBJ` | C | 1 | 0 |
| `PARTIDA` | C | 1 | 0 |
| `SUB_PAR` | C | 2 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `ENTIDAD` | C | 4 | 0 |

## `r_obj_fte_ent` (11521 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECUENCIA` | N | 8 | 0 |
| `GRUPO_OBJ` | C | 1 | 0 |
| `SUBGRP_OBJ` | C | 1 | 0 |
| `PARTIDA` | C | 1 | 0 |
| `SUBPARTIDA` | C | 2 | 0 |
| `GRUPO_FTE` | C | 1 | 0 |
| `FUENTE` | C | 2 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `ENTIDAD` | C | 4 | 0 |

## `r_obj_pry` (6778 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECUENCIA` | N | 8 | 0 |
| `GRUPO_OBJ` | C | 1 | 0 |
| `SUBGRP_OBJ` | C | 1 | 0 |
| `PARTIDA` | C | 1 | 0 |
| `SUBPARTIDA` | C | 2 | 0 |
| `PROYECTO` | C | 1 | 0 |
| `ACTIVIDAD` | C | 1 | 0 |
| `CAPT` | C | 1 | 0 |
| `NO_CAPT` | C | 1 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `ENTIDAD` | C | 4 | 0 |

## `r_obj_trf` (387 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECUENCIA` | N | 8 | 0 |
| `GRUPO_OBJ` | C | 1 | 0 |
| `SUBGRP_OBJ` | C | 1 | 0 |
| `PARTIDA` | C | 1 | 0 |
| `SUBPARTIDA` | C | 2 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `ENTIDAD` | C | 4 | 0 |

## `r_organismos` (145 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `ORGANISMO` | C | 3 | 0 |
| `GRUPO_ORG` | C | 1 | 0 |
| `SUBGRP_ORG` | C | 1 | 0 |
| `DESC` | C | 60 | 0 |
| `SIGLA` | C | 15 | 0 |

## `r_rub_ent` (1718 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECUENCIA` | N | 8 | 0 |
| `TIPO_RUBRO` | C | 2 | 0 |
| `CLASE_RUB` | C | 1 | 0 |
| `CTA_RUBRO` | C | 1 | 0 |
| `SUBCTA_RUB` | C | 1 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `ENTIDAD` | C | 4 | 0 |

## `r_rub_fte_ent` (6649 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECUENCIA` | N | 8 | 0 |
| `TIPO_RUBRO` | C | 2 | 0 |
| `CLASE_RUB` | C | 1 | 0 |
| `CUENTA_RUB` | C | 1 | 0 |
| `SUBCTA_RUB` | C | 1 | 0 |
| `GRUPO_FTE` | C | 1 | 0 |
| `FUENTE` | C | 2 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `ENTIDAD` | C | 4 | 0 |

## `r_rub_trf` (1178 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GESTION` | N | 4 | 0 |
| `SECUENCIA` | N | 8 | 0 |
| `TIPO_RUBRO` | C | 2 | 0 |
| `CLASE_RUB` | C | 1 | 0 |
| `CUENTA_RUB` | C | 1 | 0 |
| `SUBCTA_RUB` | C | 1 | 0 |
| `SECTOR_ENT` | C | 1 | 0 |
| `SUBSEC_ENT` | C | 1 | 0 |
| `AREA_ENT` | C | 1 | 0 |
| `SAREA_ENT` | C | 1 | 0 |
| `NIVEL_INS` | C | 1 | 0 |
| `ENTIDAD` | C | 4 | 0 |

## `s3aproga` (90 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `APG` | C | 25 | 0 |
| `DES` | C | 100 | 0 |
| `TIPO` | C | 1 | 0 |
| `SISIN` | C | 15 | 0 |
| `DESSISIN` | C | 60 | 0 |
| `SECTOR` | C | 6 | 0 |
| `TP_GASTO` | N | 1 | 0 |
| `FPS` | C | 2 | 0 |
| `TP_APG` | N | 1 | 0 |
| `DIRADM` | N | 3 | 0 |
| `UE` | N | 3 | 0 |
| `MACRO_DIST` | N | 6 | 0 |
| `DISTRITO` | N | 4 | 0 |
| `JUNTA` | N | 4 | 0 |
| `FUNCION` | C | 4 | 0 |
| `PND` | C | 16 | 0 |
| `TIPO_REG` | C | 1 | 0 |

## `s3asig` (156 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `USUARIO` | C | 15 | 0 |
| `TAREA` | C | 10 | 0 |

## `s3auxi` (19 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CTA` | C | 5 | 0 |
| `AUX` | C | 10 | 0 |
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `PADREA` | C | 10 | 0 |
| `RAZON` | C | 50 | 0 |
| `CIUDAD` | C | 20 | 0 |
| `TEL1` | C | 10 | 0 |
| `TEL2` | C | 10 | 0 |
| `RUC` | C | 20 | 0 |
| `SALDO` | N | 13 | 2 |
| `SALDOX` | N | 13 | 2 |
| `DBB` | N | 13 | 2 |
| `HBB` | N | 13 | 2 |
| `TIPO` | C | 1 | 0 |
| `CUENTA` | C | 20 | 0 |
| `BIT` | C | 5 | 0 |
| `TIPO_ID` | C | 1 | 0 |
| `DOCUMENTO` | C | 15 | 0 |
| `EXP_DEP` | N | 2 | 0 |

## `s3caifsa` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CASO` | C | 1 | 0 |
| `CAIF` | C | 7 | 0 |
| `DES` | C | 68 | 0 |
| `MONTO` | N | 13 | 2 |
| `TIPO` | C | 1 | 0 |

## `s3cambio` (4293 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `MONEDA` | C | 3 | 0 |
| `FECHA` | D | 8 | 0 |
| `CAMBIO` | N | 10 | 2 |
| `UFV` | N | 8 | 5 |

## `s3caypc` (1 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTD` | N | 10 | 0 |
| `DES` | C | 254 | 0 |
| `CTTO` | C | 20 | 0 |
| `TELF` | C | 100 | 0 |
| `VALOR` | N | 14 | 0 |

## `s3cbanco` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CUENTA` | C | 20 | 0 |
| `BANCO` | C | 100 | 0 |
| `SALDO` | N | 14 | 2 |

## `s3cbte` (13 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE` | C | 7 | 0 |
| `FECHA` | D | 8 | 0 |
| `CODTR` | C | 2 | 0 |
| `DOCRES` | C | 50 | 0 |
| `MONEDA` | C | 3 | 0 |
| `CAMBIO` | N | 10 | 2 |
| `USUARIO` | C | 10 | 0 |
| `BORRADOR` | C | 7 | 0 |
| `CBTER` | C | 7 | 0 |
| `CODTR1` | C | 2 | 0 |
| `FECHAIN` | D | 8 | 0 |
| `TIPO` | C | 2 | 0 |
| `BENE` | C | 140 | 0 |
| `GLOSA` | M | 10 | 0 |
| `GAS` | L | 1 | 0 |
| `REC` | L | 1 | 0 |
| `CON` | L | 1 | 0 |
| `ESTADO` | N | 1 | 0 |
| `IMP` | L | 1 | 0 |
| `TP` | C | 1 | 0 |
| `CASO` | C | 1 | 0 |
| `TDBB` | C | 16 | 0 |
| `THBB` | C | 16 | 0 |
| `UFV` | N | 8 | 5 |

## `s3cdeuda` (25 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `KEY` | C | 4 | 0 |
| `PARENT` | C | 4 | 0 |
| `TEXT` | C | 100 | 0 |
| `ACTUAL` | N | 14 | 2 |
| `ANTERIOR` | N | 14 | 2 |
| `NIVEL` | N | 2 | 0 |
| `NUEVO` | L | 1 | 0 |
| `BORRAR` | L | 1 | 0 |
| `MODIF` | L | 1 | 0 |
| `ORDEN` | N | 4 | 0 |

## `s3cdocs` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CUENTA` | C | 20 | 0 |
| `DOC` | C | 100 | 0 |
| `MONTO` | N | 14 | 2 |
| `GRUPO` | C | 50 | 0 |

## `s3cheque` (3 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE` | C | 7 | 0 |
| `LINEA` | N | 6 | 0 |
| `CTA` | C | 5 | 0 |
| `AUX` | C | 10 | 0 |
| `BENEFI` | C | 140 | 0 |
| `CHEQUE` | C | 10 | 0 |
| `MONTO` | N | 13 | 2 |

## `s3claega` (230 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CAIF` | C | 7 | 0 |
| `DES` | C | 100 | 0 |
| `TIPO` | C | 1 | 0 |

## `s3claere` (181 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CAIF` | C | 7 | 0 |
| `DES` | C | 100 | 0 |
| `TIPO` | C | 1 | 0 |

## `s3coagru` (10 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `TCOD` | C | 3 | 0 |
| `DES` | C | 50 | 0 |

## `s3codigo` (17 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CODTR` | C | 7 | 0 |
| `DES` | C | 100 | 0 |
| `T_COD` | C | 7 | 0 |
| `BITS` | C | 6 | 0 |

## `s3ctabal` (4 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA_ACT` | C | 5 | 0 |
| `CTA_PAS` | C | 5 | 0 |

## `s3ctas` (372 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CTA` | C | 5 | 0 |
| `SALDOD` | N | 13 | 2 |
| `SALDOH` | N | 13 | 2 |
| `DBB` | N | 13 | 2 |
| `HBB` | N | 13 | 2 |

## `s3ctaser` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CTA` | C | 5 | 0 |
| `DES` | C | 60 | 0 |
| `MONTO` | N | 13 | 2 |
| `TIPO` | C | 1 | 0 |

## `s3diradm0a` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `DIRADM` | N | 3 | 0 |
| `NOMBRE_DA` | C | 60 | 0 |
| `DIRECCION` | C | 60 | 0 |
| `GESTION` | N | 4 | 0 |
| `ENTIDAD` | N | 6 | 0 |
| `ORDENADOR_` | N | 3 | 0 |
| `CARGO_ORDE` | C | 60 | 0 |

## `s3distri0m` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `MACRO_DIST` | N | 4 | 0 |
| `DISTRITO` | N | 4 | 0 |
| `DESC_DISTR` | C | 60 | 0 |
| `SIGLA_DIST` | C | 3 | 0 |

## `s3et` (592 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `ET` | C | 4 | 0 |
| `DES` | C | 100 | 0 |
| `SIGLA` | C | 11 | 0 |
| `TIPO` | C | 1 | 0 |
| `INS` | C | 2 | 0 |
| `POBLACION` | N | 10 | 0 |

## `s3ff` (22 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `FF` | C | 2 | 0 |
| `DES` | C | 50 | 0 |
| `SIGLA` | C | 20 | 0 |
| `GRUPO` | C | 2 | 0 |

## `s3ff_of` (831 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `AC` | C | 2 | 0 |
| `DC` | C | 2 | 0 |
| `PR` | C | 2 | 0 |
| `GM` | C | 2 | 0 |
| `SS` | C | 2 | 0 |
| `EP` | C | 2 | 0 |
| `IF` | C | 2 | 0 |

## `s3fict` (11 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA` | C | 5 | 0 |
| `OCTA` | C | 7 | 0 |
| `DES` | C | 50 | 0 |
| `GASTO` | C | 5 | 0 |
| `RECURSO` | C | 5 | 0 |
| `TIPO` | C | 1 | 0 |

## `s3flujsa` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `FLUJO` | C | 7 | 0 |
| `MONTO` | N | 13 | 2 |
| `DESCRIP` | C | 80 | 0 |

## `s3fps` (39 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `FPS` | C | 2 | 0 |
| `DES` | C | 80 | 0 |
| `TIPO` | C | 1 | 0 |

## `s3funcion` (120 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `FUNCION` | C | 4 | 0 |
| `DES` | C | 120 | 0 |
| `TIPO` | C | 1 | 0 |

## `s3gastos` (498 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GASTO` | C | 5 | 0 |
| `DES` | C | 110 | 0 |
| `TIPO` | C | 1 | 0 |
| `ETAPA` | C | 1 | 0 |
| `AC` | C | 2 | 0 |
| `DE` | C | 2 | 0 |
| `PR` | C | 2 | 0 |
| `GM` | C | 2 | 0 |
| `SS` | C | 2 | 0 |
| `EP` | C | 2 | 0 |
| `IF` | C | 2 | 0 |
| `NP` | C | 1 | 0 |

## `s3global` (2 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GLO_NOM` | C | 100 | 0 |
| `GLO_SIG` | C | 11 | 0 |
| `GLO_TEL` | C | 30 | 0 |
| `GESTION` | C | 4 | 0 |
| `UNIDAD` | C | 3 | 0 |
| `GLO_FLAG` | N | 1 | 0 |
| `SG_FUENTES` | L | 1 | 0 |
| `AP_RECURSO` | C | 8 | 0 |
| `ALMACEN` | C | 1 | 0 |
| `BANCOS` | C | 5 | 0 |
| `CAJA` | C | 5 | 0 |
| `CXP` | C | 5 | 0 |
| `APFIN` | C | 8 | 0 |
| `APREC` | C | 8 | 0 |
| `LEVEL` | N | 1 | 0 |
| `ET` | C | 4 | 0 |
| `INS` | C | 2 | 0 |
| `FF` | C | 2 | 0 |
| `MONEDA` | C | 3 | 0 |
| `WEB` | C | 70 | 0 |
| `EMAIL` | C | 70 | 0 |
| `VERSION` | C | 10 | 0 |
| `VERIF` | N | 1 | 0 |

## `s3gr_fin` (13 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GRUPO` | C | 2 | 0 |
| `TIPO` | C | 2 | 0 |

## `s3juntas0n` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `MACRO_DIST` | N | 4 | 0 |
| `DISTRITO` | N | 4 | 0 |
| `JUNTA` | N | 4 | 0 |
| `DESC_JUNTA` | C | 60 | 0 |
| `SIGLA_JUNT` | C | 3 | 0 |

## `s3link` (4 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE_A` | C | 7 | 0 |
| `LINEA_A` | N | 6 | 0 |
| `CBTE_B` | C | 7 | 0 |
| `LINEA_B` | N | 6 | 0 |
| `ESTADO` | N | 1 | 0 |
| `DEBE` | N | 13 | 2 |
| `HABER` | N | 13 | 2 |
| `COMP_TIP` | C | 5 | 0 |

## `s3macdis0l` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `DEPARTAMEN` | N | 2 | 0 |
| `PROVINCIA` | N | 3 | 0 |
| `SECCION_PR` | N | 4 | 0 |
| `MACRO_DIST` | N | 4 | 0 |
| `DESC_MDIST` | C | 60 | 0 |
| `SIGLA_MDIS` | C | 3 | 0 |

## `s3mat` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `NIVEL` | C | 1 | 0 |
| `TESO` | C | 3 | 0 |
| `GASTO` | C | 5 | 0 |
| `RECURSO` | C | 5 | 0 |
| `CTA` | C | 7 | 0 |
| `TIPO` | C | 1 | 0 |
| `PRO_M01` | N | 13 | 2 |
| `EJE_M01` | N | 13 | 2 |
| `PRO_M01S1` | N | 13 | 2 |
| `EJE_M01S1` | N | 13 | 2 |
| `PRO_M01S2` | N | 13 | 2 |
| `EJE_M01S2` | N | 13 | 2 |
| `PRO_M01S3` | N | 13 | 2 |
| `EJE_M01S3` | N | 13 | 2 |
| `PRO_M01S4` | N | 13 | 2 |
| `EJE_M01S4` | N | 13 | 2 |
| `PRO_M01S5` | N | 13 | 2 |
| `EJE_M01S5` | N | 13 | 2 |
| `PRO_M02` | N | 13 | 2 |
| `EJE_M02` | N | 13 | 2 |
| `PRO_M02S1` | N | 13 | 2 |
| `EJE_M02S1` | N | 13 | 2 |
| `PRO_M02S2` | N | 13 | 2 |
| `EJE_M02S2` | N | 13 | 2 |
| `PRO_M02S3` | N | 13 | 2 |
| `EJE_M02S3` | N | 13 | 2 |
| `PRO_M02S4` | N | 13 | 2 |
| `EJE_M02S4` | N | 13 | 2 |
| `PRO_M02S5` | N | 13 | 2 |
| `EJE_M02S5` | N | 13 | 2 |
| `PRO_M03` | N | 13 | 2 |
| `EJE_M03` | N | 13 | 2 |
| `PRO_M03S1` | N | 13 | 2 |
| `EJE_M03S1` | N | 13 | 2 |
| `PRO_M03S2` | N | 13 | 2 |
| `EJE_M03S2` | N | 13 | 2 |
| `PRO_M03S3` | N | 13 | 2 |
| `EJE_M03S3` | N | 13 | 2 |
| `PRO_M03S4` | N | 13 | 2 |
| `EJE_M03S4` | N | 13 | 2 |
| `PRO_M03S5` | N | 13 | 2 |
| `EJE_M03S5` | N | 13 | 2 |
| `PRO_M04` | N | 13 | 2 |
| `EJE_M04` | N | 13 | 2 |
| `PRO_M04S1` | N | 13 | 2 |
| `EJE_M04S1` | N | 13 | 2 |
| `PRO_M04S2` | N | 13 | 2 |
| `EJE_M04S2` | N | 13 | 2 |
| `PRO_M04S3` | N | 13 | 2 |
| `EJE_M04S3` | N | 13 | 2 |
| `PRO_M04S4` | N | 13 | 2 |
| `EJE_M04S4` | N | 13 | 2 |
| `PRO_M04S5` | N | 13 | 2 |
| `EJE_M04S5` | N | 13 | 2 |
| `PRO_M05` | N | 13 | 2 |
| `EJE_M05` | N | 13 | 2 |
| `PRO_M05S1` | N | 13 | 2 |
| `EJE_M05S1` | N | 13 | 2 |
| `PRO_M05S2` | N | 13 | 2 |
| `EJE_M05S2` | N | 13 | 2 |
| `PRO_M05S3` | N | 13 | 2 |
| `EJE_M05S3` | N | 13 | 2 |
| `PRO_M05S4` | N | 13 | 2 |
| `EJE_M05S4` | N | 13 | 2 |
| `PRO_M05S5` | N | 13 | 2 |
| `EJE_M05S5` | N | 13 | 2 |
| `PRO_M06` | N | 13 | 2 |
| `EJE_M06` | N | 13 | 2 |
| `PRO_M06S1` | N | 13 | 2 |
| `EJE_M06S1` | N | 13 | 2 |
| `PRO_M06S2` | N | 13 | 2 |
| `EJE_M06S2` | N | 13 | 2 |
| `PRO_M06S3` | N | 13 | 2 |
| `EJE_M06S3` | N | 13 | 2 |
| `PRO_M06S4` | N | 13 | 2 |
| `EJE_M06S4` | N | 13 | 2 |
| `PRO_M06S5` | N | 13 | 2 |
| `EJE_M06S5` | N | 13 | 2 |
| `PRO_M07` | N | 13 | 2 |
| `EJE_M07` | N | 13 | 2 |
| `PRO_M07S1` | N | 13 | 2 |
| `EJE_M07S1` | N | 13 | 2 |
| `PRO_M07S2` | N | 13 | 2 |
| `EJE_M07S2` | N | 13 | 2 |
| `PRO_M07S3` | N | 13 | 2 |
| `EJE_M07S3` | N | 13 | 2 |
| `PRO_M07S4` | N | 13 | 2 |
| `EJE_M07S4` | N | 13 | 2 |
| `PRO_M07S5` | N | 13 | 2 |
| `EJE_M07S5` | N | 13 | 2 |
| `PRO_M08` | N | 13 | 2 |
| `EJE_M08` | N | 13 | 2 |
| `PRO_M08S1` | N | 13 | 2 |
| `EJE_M08S1` | N | 13 | 2 |
| `PRO_M08S2` | N | 13 | 2 |
| `EJE_M08S2` | N | 13 | 2 |
| `PRO_M08S3` | N | 13 | 2 |
| `EJE_M08S3` | N | 13 | 2 |
| `PRO_M08S4` | N | 13 | 2 |
| `EJE_M08S4` | N | 13 | 2 |
| `PRO_M08S5` | N | 13 | 2 |
| `EJE_M08S5` | N | 13 | 2 |
| `PRO_M09` | N | 13 | 2 |
| `EJE_M09` | N | 13 | 2 |
| `PRO_M09S1` | N | 13 | 2 |
| `EJE_M09S1` | N | 13 | 2 |
| `PRO_M09S2` | N | 13 | 2 |
| `EJE_M09S2` | N | 13 | 2 |
| `PRO_M09S3` | N | 13 | 2 |
| `EJE_M09S3` | N | 13 | 2 |
| `PRO_M09S4` | N | 13 | 2 |
| `EJE_M09S4` | N | 13 | 2 |
| `PRO_M09S5` | N | 13 | 2 |
| `EJE_M09S5` | N | 13 | 2 |
| `PRO_M10` | N | 13 | 2 |
| `EJE_M10` | N | 13 | 2 |
| `PRO_M10S1` | N | 13 | 2 |
| `EJE_M10S1` | N | 13 | 2 |
| `PRO_M10S2` | N | 13 | 2 |
| `EJE_M10S2` | N | 13 | 2 |
| `PRO_M10S3` | N | 13 | 2 |
| `EJE_M10S3` | N | 13 | 2 |
| `PRO_M10S4` | N | 13 | 2 |
| `EJE_M10S4` | N | 13 | 2 |
| `PRO_M10S5` | N | 13 | 2 |
| `EJE_M10S5` | N | 13 | 2 |
| `PRO_M11` | N | 13 | 2 |
| `EJE_M11` | N | 13 | 2 |
| `PRO_M11S1` | N | 13 | 2 |
| `EJE_M11S1` | N | 13 | 2 |
| `PRO_M11S2` | N | 13 | 2 |
| `EJE_M11S2` | N | 13 | 2 |
| `PRO_M11S3` | N | 13 | 2 |
| `EJE_M11S3` | N | 13 | 2 |
| `PRO_M11S4` | N | 13 | 2 |
| `EJE_M11S4` | N | 13 | 2 |
| `PRO_M11S5` | N | 13 | 2 |
| `EJE_M11S5` | N | 13 | 2 |
| `PRO_M12` | N | 13 | 2 |
| `EJE_M12` | N | 13 | 2 |
| `PRO_M12S1` | N | 13 | 2 |
| `EJE_M12S1` | N | 13 | 2 |
| `PRO_M12S2` | N | 13 | 2 |
| `EJE_M12S2` | N | 13 | 2 |
| `PRO_M12S3` | N | 13 | 2 |
| `EJE_M12S3` | N | 13 | 2 |
| `PRO_M12S4` | N | 13 | 2 |
| `EJE_M12S4` | N | 13 | 2 |
| `PRO_M12S5` | N | 13 | 2 |
| `EJE_M12S5` | N | 13 | 2 |

## `s3moneda` (2 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `MONEDA` | C | 3 | 0 |
| `DES` | C | 50 | 0 |

## `s3movco` (24 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE` | C | 7 | 0 |
| `LINEA` | N | 6 | 0 |
| `FECHA` | D | 8 | 0 |
| `CODTR` | C | 2 | 0 |
| `CODTR1` | C | 2 | 0 |
| `GARECO` | C | 1 | 0 |
| `CTA` | C | 5 | 0 |
| `AUX` | C | 10 | 0 |
| `OEC` | C | 3 | 0 |
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `DBB` | N | 13 | 2 |
| `HBB` | N | 13 | 2 |
| `DBE` | N | 13 | 2 |
| `HBE` | N | 13 | 2 |
| `TESO` | C | 3 | 0 |
| `ESTADO` | N | 1 | 0 |

## `s3movga` (375 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE` | C | 7 | 0 |
| `LINEA` | N | 6 | 0 |
| `FECHA` | D | 8 | 0 |
| `CODTR` | C | 2 | 0 |
| `CODTR1` | C | 2 | 0 |
| `AP` | C | 25 | 0 |
| `GASTO` | C | 5 | 0 |
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `ET` | C | 4 | 0 |
| `OEC` | C | 3 | 0 |
| `DBB` | N | 13 | 2 |
| `HBB` | N | 13 | 2 |
| `DBE` | N | 13 | 2 |
| `HBE` | N | 13 | 2 |
| `CLASEG` | C | 5 | 0 |
| `ESTADO` | N | 1 | 0 |

## `s3movpa` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE` | C | 7 | 0 |
| `LINEA` | N | 6 | 0 |
| `FECHA` | D | 8 | 0 |
| `CODTR` | C | 2 | 0 |
| `CODTR1` | C | 2 | 0 |
| `AP` | C | 8 | 0 |
| `GASTO` | C | 5 | 0 |
| `FF` | C | 7 | 0 |
| `OF` | C | 7 | 0 |
| `RECURSO` | C | 5 | 0 |
| `CTA` | C | 7 | 0 |
| `AUX` | C | 10 | 0 |
| `TESO` | C | 3 | 0 |
| `DBB` | N | 13 | 2 |
| `HBB` | N | 13 | 2 |
| `DBE` | N | 13 | 2 |
| `HBE` | N | 13 | 2 |
| `ESTADO` | N | 1 | 0 |

## `s3movre` (20 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE` | C | 7 | 0 |
| `LINEA` | N | 6 | 0 |
| `FECHA` | D | 8 | 0 |
| `CODTR` | C | 2 | 0 |
| `CODTR1` | C | 2 | 0 |
| `RECURSO` | C | 5 | 0 |
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `ET` | C | 4 | 0 |
| `OEC` | C | 3 | 0 |
| `DBB` | N | 13 | 2 |
| `HBB` | N | 13 | 2 |
| `DBE` | N | 13 | 2 |
| `HBE` | N | 13 | 2 |
| `CLASER` | C | 5 | 0 |
| `ESTADO` | N | 1 | 0 |

## `s3msg` (36 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `MSG` | C | 5 | 0 |
| `DET` | M | 10 | 0 |

## `s3of` (156 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `OF` | C | 3 | 0 |
| `DES` | C | 100 | 0 |
| `SIGLA` | C | 15 | 0 |

## `s3pagos` (72 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA` | C | 5 | 0 |
| `OCTA` | C | 7 | 0 |
| `RECURSO` | C | 5 | 0 |
| `MODALIDAD` | C | 1 | 0 |

## `s3parametros` (3 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `ENTIDAD` | C | 4 | 0 |
| `RESTRIC` | C | 2 | 0 |
| `DESC` | C | 100 | 0 |

## `s3pg_sfo` (970 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `GASTO` | C | 5 | 0 |
| `OEC` | C | 3 | 0 |

## `s3plan_c` (372 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA` | C | 5 | 0 |
| `DES` | C | 100 | 0 |
| `TIPO` | C | 1 | 0 |
| `AUX` | C | 1 | 0 |
| `NIVEL` | N | 2 | 0 |
| `NOTABG` | C | 10 | 0 |
| `NOTAER` | C | 10 | 0 |
| `AUX_BASE` | C | 13 | 0 |

## `s3pnd` (296 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `PND` | C | 16 | 0 |
| `DESC_PND` | C | 150 | 0 |
| `NIVEL` | C | 1 | 0 |

## `s3pr_sfo` (342 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `RECURSO` | C | 5 | 0 |
| `OEC` | C | 3 | 0 |

## `s3pre_ga` (366 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `APG` | C | 25 | 0 |
| `GASTO` | C | 5 | 0 |
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `ET` | C | 4 | 0 |
| `ASIGMN1` | N | 13 | 2 |
| `ASIGME1` | N | 13 | 2 |
| `ASIGMN2` | N | 13 | 2 |
| `ASIGME2` | N | 13 | 2 |
| `ASIGMN3` | N | 13 | 2 |
| `ASIGME3` | N | 13 | 2 |
| `ASIGMN4` | N | 13 | 2 |
| `ASIGME4` | N | 13 | 2 |
| `TRASMN` | N | 13 | 2 |
| `TRASME` | N | 13 | 2 |
| `COMPRMN` | N | 13 | 2 |
| `COMPRME` | N | 13 | 2 |
| `DEVENMN` | N | 13 | 2 |
| `DEVENME` | N | 13 | 2 |
| `PAGOMN` | N | 13 | 2 |
| `PAGOME` | N | 13 | 2 |
| `CONSUMN` | N | 13 | 2 |
| `CONSUME` | N | 13 | 2 |

## `s3pre_re` (17 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `RECURSO` | C | 5 | 0 |
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `ET` | C | 4 | 0 |
| `ASIGMN1` | N | 13 | 2 |
| `ASIGME1` | N | 13 | 2 |
| `ASIGMN2` | N | 13 | 2 |
| `ASIGME2` | N | 13 | 2 |
| `ASIGMN3` | N | 13 | 2 |
| `ASIGME3` | N | 13 | 2 |
| `ASIGMN4` | N | 13 | 2 |
| `ASIGME4` | N | 13 | 2 |
| `TRASMN` | N | 13 | 2 |
| `TRASME` | N | 13 | 2 |
| `DEVENMN` | N | 13 | 2 |
| `DEVENME` | N | 13 | 2 |
| `INCMN` | N | 13 | 2 |
| `INCME` | N | 13 | 2 |

## `s3recur` (350 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `RECURSO` | C | 5 | 0 |
| `DES` | C | 100 | 0 |
| `TIPO` | C | 1 | 0 |
| `AC` | C | 2 | 0 |
| `DE` | C | 2 | 0 |
| `PR` | C | 2 | 0 |
| `GM` | C | 2 | 0 |
| `SS` | C | 2 | 0 |
| `EP` | C | 2 | 0 |
| `IF` | C | 2 | 0 |
| `NP` | C | 1 | 0 |

## `s3relga` (1022 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA` | C | 5 | 0 |
| `GASTO` | C | 5 | 0 |
| `CAIF` | C | 7 | 0 |
| `TIPO` | C | 1 | 0 |
| `AC` | C | 2 | 0 |
| `DE` | C | 2 | 0 |
| `PR` | C | 2 | 0 |
| `GM` | C | 2 | 0 |
| `SS` | C | 2 | 0 |
| `EP` | C | 2 | 0 |
| `IF` | C | 2 | 0 |
| `APX` | C | 1 | 0 |

## `s3relre` (311 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA` | C | 5 | 0 |
| `RECURSO` | C | 5 | 0 |
| `CAIF` | C | 7 | 0 |
| `TIPO` | C | 1 | 0 |
| `AC` | C | 2 | 0 |
| `DE` | C | 2 | 0 |
| `PR` | C | 2 | 0 |
| `GM` | C | 2 | 0 |
| `SS` | C | 2 | 0 |
| `EP` | C | 2 | 0 |
| `IF` | C | 2 | 0 |

## `s3restri` (27 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CODTR` | C | 2 | 0 |
| `CTA` | C | 5 | 0 |
| `OCTA` | C | 7 | 0 |
| `DH` | C | 1 | 0 |

## `s3safco` (715 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `OEC` | C | 14 | 0 |
| `DESCRIP` | C | 100 | 0 |
| `TIPO` | C | 1 | 0 |

## `s3sector` (241 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `SECTOR` | C | 6 | 0 |
| `GRUPO` | C | 2 | 0 |
| `DES` | C | 100 | 0 |
| `SIGLA` | C | 14 | 0 |
| `TIPO` | C | 7 | 0 |

## `s3situac` (5 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE` | C | 7 | 0 |
| `LINEA` | N | 6 | 0 |
| `TIPO` | C | 1 | 0 |
| `CODTR` | C | 2 | 0 |
| `ESTADO` | N | 1 | 0 |
| `AP` | C | 25 | 0 |
| `PART` | C | 5 | 0 |
| `FF` | C | 2 | 0 |
| `OF` | C | 3 | 0 |
| `ET` | C | 3 | 0 |
| `CTA` | C | 5 | 0 |
| `AUX` | C | 10 | 0 |
| `DEBE_AC` | N | 13 | 2 |
| `HABER_AC` | N | 13 | 2 |
| `DEBE_TOT` | N | 13 | 2 |
| `HABER_TOT` | N | 13 | 2 |

## `s3tareas` (154 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `TAREA` | C | 10 | 0 |
| `DES` | C | 60 | 0 |

## `s3tesosa` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `GASTO` | C | 5 | 0 |
| `RECURSO` | C | 5 | 0 |
| `DES` | C | 80 | 0 |
| `MONTO` | N | 13 | 2 |
| `TIPO` | C | 1 | 0 |

## `s3unidad` (1 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `DESC` | C | 50 | 0 |
| `CIUDAD` | C | 25 | 0 |
| `CBTE_VALI` | N | 7 | 0 |
| `CBTE_BORR` | N | 7 | 0 |
| `SALDOOK` | L | 1 | 0 |
| `SALDO_P` | N | 13 | 2 |
| `SALDO_E` | N | 13 | 2 |
| `EMPRESA` | N | 1 | 0 |
| `UOD` | N | 2 | 0 |
| `SFPM` | C | 7 | 0 |
| `EFE24` | N | 2 | 0 |
| `FLUJOINI` | N | 14 | 2 |
| `FLUJO24` | N | 14 | 2 |
| `TIPO_REG` | C | 1 | 0 |
| `SALINI` | N | 2 | 0 |

## `s3unieje0b` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `DIRADM` | N | 3 | 0 |
| `UE` | N | 3 | 0 |
| `DESC_UE` | C | 60 | 0 |
| `DIRECCION` | C | 60 | 0 |
| `ORDENADOR_` | N | 3 | 0 |

## `s3usrid` (1 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `USUARIO` | C | 15 | 0 |
| `DES` | C | 50 | 0 |
| `PSW` | C | 15 | 0 |
| `TIPO` | C | 1 | 0 |

## `s4log` (4 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `FECHA` | D | 8 | 0 |
| `HORA` | C | 10 | 0 |
| `USUARIO` | C | 10 | 0 |
| `TIPO` | C | 1 | 0 |
| `DESC` | M | 10 | 0 |

## `s5caifgas` (1023 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA` | C | 5 | 0 |
| `GASTO` | C | 5 | 0 |
| `CAIF` | C | 7 | 0 |
| `TIPO` | C | 1 | 0 |
| `AC` | C | 2 | 0 |
| `DE` | C | 2 | 0 |
| `PR` | C | 2 | 0 |
| `GM` | C | 2 | 0 |
| `SS` | C | 2 | 0 |
| `EP` | C | 2 | 0 |
| `IF` | C | 2 | 0 |
| `APX` | C | 1 | 0 |

## `s5caifrec` (320 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA` | C | 5 | 0 |
| `RECURSO` | C | 5 | 0 |
| `CAIF` | C | 7 | 0 |
| `TIPO` | C | 1 | 0 |
| `AC` | C | 2 | 0 |
| `DE` | C | 2 | 0 |
| `PR` | C | 2 | 0 |
| `GM` | C | 2 | 0 |
| `SS` | C | 2 | 0 |
| `EP` | C | 2 | 0 |
| `IF` | C | 2 | 0 |

## `s5flujo` (384 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `FLUJO` | C | 7 | 0 |
| `DES` | C | 100 | 0 |
| `TIPO` | C | 1 | 0 |

## `s5flujogas` (782 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA` | C | 5 | 0 |
| `GASTO` | C | 5 | 0 |
| `FLUJO` | C | 7 | 0 |
| `TIPO` | C | 1 | 0 |
| `AC` | C | 2 | 0 |
| `DE` | C | 2 | 0 |
| `PR` | C | 2 | 0 |
| `GM` | C | 2 | 0 |
| `SS` | C | 2 | 0 |
| `EP` | C | 2 | 0 |
| `IF` | C | 2 | 0 |
| `APX` | C | 1 | 0 |

## `s5flujorec` (235 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CTA` | C | 5 | 0 |
| `RECURSO` | C | 5 | 0 |
| `FLUJO` | C | 7 | 0 |
| `TIPO` | C | 1 | 0 |
| `AC` | C | 2 | 0 |
| `DE` | C | 2 | 0 |
| `PR` | C | 2 | 0 |
| `GM` | C | 2 | 0 |
| `SS` | C | 2 | 0 |
| `EP` | C | 2 | 0 |
| `IF` | C | 2 | 0 |

## `s6bancos` (51 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `BANCO` | N | 5 | 0 |
| `DESC_BANCO` | C | 40 | 0 |
| `SIGLA` | C | 3 | 0 |

## `s6cbte_bene` (11 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE` | C | 7 | 0 |
| `TIPO_ID` | C | 1 | 0 |
| `DOCUMENTO` | C | 15 | 0 |
| `EXP_DEP` | N | 2 | 0 |

## `s6clase_gasto` (250 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `CLASE` | I | 4 | 0 |
| `DESC_CLASE` | C | 50 | 0 |
| `OBJETO` | C | 5 | 0 |
| `DESC_OBJ` | C | 100 | 0 |

## `s6depositos` (4 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CBTE` | C | 7 | 0 |
| `LINEA` | N | 6 | 0 |
| `CTA` | C | 5 | 0 |
| `AUX` | C | 10 | 0 |
| `DEPO` | C | 140 | 0 |
| `NRO_DEP` | C | 12 | 0 |
| `MONTO` | N | 13 | 2 |
| `FECHA_DEP` | D | 8 | 0 |

## `s6rango_cheque` (3 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `CUENTA` | C | 20 | 0 |
| `TALONARIO` | N | 8 | 0 |
| `R_DESDE` | N | 12 | 0 |
| `R_HASTA` | N | 12 | 0 |
| `F_ACTIVA` | D | 8 | 0 |
| `F_DESAC` | D | 8 | 0 |
| `ESTADO` | L | 1 | 0 |

## `s7benef` (4 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `UNIDAD` | C | 3 | 0 |
| `BENEF` | N | 7 | 0 |
| `TIPO_ID` | C | 1 | 0 |
| `DOCUMENTO` | C | 15 | 0 |
| `EXP_DEP` | N | 2 | 0 |
| `PATERNO` | C | 40 | 0 |
| `MATERNO` | C | 40 | 0 |
| `AP_CASADA` | C | 40 | 0 |
| `NOMBRES` | C | 60 | 0 |
| `RAZON_SOC` | C | 170 | 0 |
| `TIPO` | C | 1 | 0 |
| `MAIL` | C | 100 | 0 |

## `semanal` (0 registros)

| Campo | Tipo | Largo | Dec |
|---|---|---|---|
| `ENTIDAD` | C | 10 | 0 |
| `LOTE_WEEK` | C | 10 | 0 |
| `LOTE` | C | 10 | 0 |
