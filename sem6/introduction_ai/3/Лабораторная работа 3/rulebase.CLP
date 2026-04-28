(defrule data-input
  (initial-fact)
=>
  (printout t crlf "Введите число дней до зачета (целое значение): ")
  (bind ?days (read))

 (if (numberp ?days) 
	then (assert (days ?days))
	else (printout t "ВВедите число" crlf))


  (printout t crlf "Введите число несделанных лабораторных работ (в %) ")
  (bind ?works (read))
  (assert (works ?works)))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;(defrule test
; (days ?days)
; (works ?works)
;=>
;(printout t crlf crlf "ПРОВЕРКА" crlf)
;(assert (freetime "no")))

(defrule R1
	(days ?days)
	(works ?works)
	(test (and (= ?days 1) (<> ?works 0))) 
=>
(printout t crlf crlf "Свободного времени нет" crlf)
(assert (freetime "no")))

(defrule R2
	(days ?days)
	(works ?works)
	(test (and (= ?days 2) (>= ?works 10))) 
=>
(printout t crlf crlf "Свободного времени нет" crlf)
(assert (freetime "no")))

(defrule R3
	(days ?days)
	(works ?works)
	(test (and (= ?days 2) (< ?works 10))) 
=>
(printout t crlf crlf "Свободного времени мало" crlf)
(assert (freetime "a-little")))

(defrule R4
	(days ?days)
	(works ?works)
	(test (and (= ?days 3) (> ?works 25))) 
=>
(printout t crlf crlf "Свободного времени нет" crlf)
(assert (freetime "no")))

;RULE:   R5
;        IF:     days = 3 AND works <= 25 AND works > 10
;        THEN:   fretim = "little"
;RULE:   R6
;        IF:     days = 3 AND works <= 10
;        THEN:   fretim = "many"
;RULE:   R7
;        IF:     days = 4 AND works < 25
;        THEN:   fretim = "many"
;RULE:   R8
;        IF:     days = 4 AND works >= 25 AND works < 75
;        THEN:   fretim = "little"
;RULE:   R9
;        IF:     days = 4 AND works >= 75
;	THEN:	fretim = "no"
;RULE:   R10
;        IF:     days = 5 AND works < 60
;        THEN:   fretim = "many"
;RULE:   R11
;        IF:     days = 5 AND works >= 60 AND works < 90
;        THEN:   fretim = "little"
;RULE:   R12
;        IF:     days = 5 AND works >= 90
;	THEN:	fretim = "no"
;RULE:   R13
;        IF:     days > 5
;        THEN:   fretim = "many"

