(defrule vvod_dannix
 (initial-fact)
  =>
  (printout t crlf "Введите объем винчестеров:")
  (bind ?ob (read))

  (if (numberp ?days) 
	then (assert (days ?days))
	else (printout t "ошибка" crlf))

  (printout t crlf "Введите тип RAID:")
  (bind ?RAID (read))
  (assert (RAID ?RAID))

  (printout t crlf "Введите число процессоров:")
  (bind ?proc (read))
  (assert (proc ?proc))

  (printout t crlf "Введите число ядер:")
  (bind ?core (read))
  (assert (core ?core))

  (printout t crlf "Есть ли ИБП?")
  (bind ?UPS (read))
  (assert (UPS ?UPS))
)
---------------------------------------------------
(defrule Obm_disc1
 (test(and(> ?ob 0)(<= ?ob 250)(= ?RAID 0)))
  =>
 (assert (ur_serv small))
)
(defrule Obm_disc2
 (test(and(> ?ob 250)(<= ?ob 1000)(= ?RAID 0)))
  =>
 (assert (ur_serv standart))
)
(defrule Obm_disc3
 (test(and(> ?ob 1000)(= ?RAID 0)))
  =>
 (assert (ur_serv big))
)
(defrule Obm_disc4
 (test(and(> ?ob 0)(<= ?ob 250)(= ?RAID 1)))
  =>
 (assert (ur_serv small))
)
(defrule Obm_disc5
 (test(and(> ?ob 250)(<= ?ob 1000)(= ?RAID 1)))
  =>
 (assert (ur_serv standart))
)
(defrule Obm_disc6
 (test(and(> ?ob 1000)(= ?RAID 1)))
  =>
 (assert (ur_serv big))
)
(defrule Obm_disc7
 (test(and(> ?ob 0)(<= ?ob 250)(= ?RAID 5)))
  =>
 (assert (ur_serv small))
)
(defrule Obm_disc8
 (test(and(> ?ob 250)(<= ?ob 1000)(= ?RAID 5)))
  =>
 (assert (ur_serv standart))
)
(defrule Obm_disc9
 (test(and(> ?ob 1000)(= ?RAID 5)))
  =>
 (assert (ur_serv big))
)
-------------------------------------------------
(defrule har_serv1
 (test(and(= ?proc 1)(>= ?core 1) (<= ?core 2)))
  =>
 (assert (mosh_serv malomoshn))
)
(defrule har_serv2
 (test(and(= ?proc 1)(>= ?core 3) (<= ?core 8)))
  =>
 (assert (mosh_serv srednemoshn))
)
(defrule har_serv3
 (test(and(= ?proc 1)(> ?core 8)))
  =>
 (assert (mosh_serv moshn))
)
(defrule har_serv4
 (test(and(= ?proc 2)(>= ?core 1) (<= ?core 2)))
  =>
 (assert (mosh_serv malomoshn))
)
(defrule har_serv5
 (test(and(= ?proc 2)(>= ?core 3) (<= ?core 8)))
  =>
 (assert (mosh_serv srednemoshn))
)
(defrule har_serv6
 (test(and(= ?proc 2)(> ?core 8)))
  =>
 (assert (mosh_serv moshn))
)
(defrule har_serv7
 (test(and(> ?proc 2)(>= ?core 1) (<= ?core 2)))
  =>
 (assert (mosh_serv moshn))
)
(defrule har_serv8
 (test(and(> ?proc 2)(>= ?core 3) (<= ?core 8)))
  =>
 (assert (mosh_serv moshn))
)
(defrule har_serv9
 (test(and(> ?proc 2)(> ?core 8)))
  =>
 (assert (mosh_serv moshn))
)
----------------------------------------------------
(defrule obsh_har_serv1
 (ur_serv small)
 (mosh_serv malomoshn)
 (UPS yes)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv2
 (ur_serv small)
 (mosh_serv malomoshn)
 (UPS no)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv3
 (ur_serv standart)
 (mosh_serv malomoshn)
 (UPS yes)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv4
 (ur_serv standart)
 (mosh_serv malomoshn)
 (UPS no)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)

(defrule obsh_har_serv5
 (ur_serv big)
 (mosh_serv malomoshn)
 (UPS yes)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv6
 (ur_serv big)
 (mosh_serv malomoshn)
 (UPS no)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)

//////////////////////////////
(defrule obsh_har_serv7
 (ur_serv small)
 (mosh_serv srednemoshn)
 (UPS yes)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv8
 (ur_serv small)
 (mosh_serv srednemoshn)
 (UPS no)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv9
 (ur_serv standart)
 (mosh_serv srednemoshn)
 (UPS yes)
  =>
 (printout t crlf "сервер предприятия" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv10
 (ur_serv standart)
 (mosh_serv srednemoshn)
 (UPS no)
  =>
 (printout t crlf "сервер предприятия" crlf)
 (assert (ob_har serv_otdela))
)

(defrule obsh_har_serv11
 (ur_serv big)
 (mosh_serv srednemoshn)
 (UPS yes)
  =>
 (printout t crlf "сервер предприятия" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv12
 (ur_serv big)
 (mosh_serv srednemoshn)
 (UPS no)
  =>
 (printout t crlf "сервер предприятия" crlf)
 (assert (ob_har serv_otdela))
)
///////////////////////////////////////////
(defrule obsh_har_serv13
 (ur_serv small)
 (mosh_serv moshn)
 (UPS yes)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv14
 (ur_serv small)
 (mosh_serv moshn)
 (UPS no)
  =>
 (printout t crlf "сервер отдела" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv15
 (ur_serv standart)
 (mosh_serv moshn)
 (UPS yes)
  =>
 (printout t crlf "сервер сервер" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv16
 (ur_serv standart)
 (mosh_serv moshn)
 (UPS no)
  =>
 (printout t crlf "сервер предприятия" crlf)
 (assert (ob_har serv_otdela))
)

(defrule obsh_har_serv17
 (ur_serv big)
 (mosh_serv moshn)
 (UPS yes)
  =>
 (printout t crlf "сервер data-центра" crlf)
 (assert (ob_har serv_otdela))
)
(defrule obsh_har_serv18
 (ur_serv big)
 (mosh_serv moshn)
 (UPS no)
  =>
 (printout t crlf "сервер data-центра" crlf)
 (assert (ob_har serv_otdela))
)
