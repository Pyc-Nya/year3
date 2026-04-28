; ============================================================
; Lab 3
; Expert system: employment chance estimation
; ============================================================

(deffacts input-data
   (experience junior)
   (education courses)
   (company big)
   (salary high)
)

; ============================================================

; specialist-level rules
(defrule specialist-level-1
   (experience junior)
   (education none)
=>
   (assert (specialist-level low))
)

(defrule specialist-level-2
   (experience junior)
   (education courses)
=>
   (assert (specialist-level low))
)

(defrule specialist-level-3
   (experience junior)
   (education higher)
=>
   (assert (specialist-level medium))
)

(defrule specialist-level-4
   (experience middle)
   (education none)
=>
   (assert (specialist-level medium))
)

(defrule specialist-level-5
   (experience middle)
   (education courses)
=>
   (assert (specialist-level medium))
)

(defrule specialist-level-6
   (experience middle)
   (education higher)
=>
   (assert (specialist-level high))
)

(defrule specialist-level-7
   (experience senior)
   (education none)
=>
   (assert (specialist-level high))
)

(defrule specialist-level-8
   (experience senior)
   (education courses)
=>
   (assert (specialist-level high))
)

(defrule specialist-level-9
   (experience senior)
   (education higher)
=>
   (assert (specialist-level high))
)

; ============================================================

; competition rules

(defrule competition-1
   (company big)
   (salary high)
=>
   (assert (competition high))
)

(defrule competition-2
   (company big)
   (salary medium)
=>
   (assert (competition high))
)

(defrule competition-3
   (company big)
   (salary low)
=>
   (assert (competition medium))
)

(defrule competition-4
   (company medium)
   (salary high)
=>
   (assert (competition high))
)

(defrule competition-5
   (company medium)
   (salary medium)
=>
   (assert (competition medium))
)

(defrule competition-6
   (company medium)
   (salary low)
=>
   (assert (competition low))
)

(defrule competition-7
   (company startup)
   (salary high)
=>
   (assert (competition medium))
)

(defrule competition-8
   (company startup)
   (salary medium)
=>
   (assert (competition medium))
)

(defrule competition-9
   (company startup)
   (salary low)
=>
   (assert (competition low))
)


; ============================================================

; employment-chance rules

(defrule employment-chance-1
   (specialist-level low)
   (competition high)
=>
   (assert (employment-chance 1))
)

(defrule employment-chance-2
   (specialist-level low)
   (competition medium)
=>
   (assert (employment-chance 2))
)

(defrule employment-chance-3
   (specialist-level low)
   (competition low)
=>
   (assert (employment-chance 3))
)

(defrule employment-chance-4
   (specialist-level medium)
   (competition high)
=>
   (assert (employment-chance 2))
)

(defrule employment-chance-5
   (specialist-level medium)
   (competition medium)
=>
   (assert (employment-chance 3))
)

(defrule employment-chance-6
   (specialist-level medium)
   (competition low)
=>
   (assert (employment-chance 4))
)

(defrule employment-chance-7
   (specialist-level high)
   (competition high)
=>
   (assert (employment-chance 3))
)

(defrule employment-chance-8
   (specialist-level high)
   (competition medium)
=>
   (assert (employment-chance 4))
)

(defrule employment-chance-9
   (specialist-level high)
   (competition low)
=>
   (assert (employment-chance 5))
)

