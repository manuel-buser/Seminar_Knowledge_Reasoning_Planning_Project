;; ============================================================================
;;  Spider (axioms) — instance i01
;;
;;  Configuration: 1 deck, 3 suits, 3 values per suit, 3 piles, 1 deal of 3
;;  cards (deal-1 used as a no-card sentinel for NEXT-DEAL).
;;  Total cards: 9. Suit numbering 0..2; value numbering 0=Ace, 1=Queen, 2=King.
;;
;;  Initial layout — already a "win-shaped" puzzle:
;;    pile-0:  K_s0 (bottom), Q_s0 (top, clear)
;;    pile-1:  K_s1 (bottom), Q_s1 (top, clear)
;;    pile-2:  K_s2 (bottom), Q_s2 (top, clear)
;;    deal-0 stack (bottom-up): deal-0, A_s2, A_s1, A_s0 (top, clear).
;;
;;  After one start-dealing + three deal-card + finish-dealing, every pile holds
;;  a properly built A-Q-K run. Three start-collecting-deck actions then harvest
;;  all suits to discard.
;;
;;  Expected optimal cost: 4
;;     = 1 (start-dealing) + 3 × 1 (start-collecting-deck).
;;  Expected plan length: ~17 actions (the rest are zero-cost cascade steps).
;;
;;  This is a deliberate sanity instance for the axioms encoding. Translating
;;  it back to the no-axioms encoding (re-adding init facts for movable and
;;  part-of-tableau) must yield the same optimal cost = 4. That is the
;;  equivalence test.
;; ============================================================================

(define (problem spider-axioms-1-3-3-3-1-001)
(:domain spider-axioms)

(:objects
    card-d0-s0-v0 - card    ;; A_s0
    card-d0-s0-v1 - card    ;; Q_s0
    card-d0-s0-v2 - card    ;; K_s0
    card-d0-s1-v0 - card    ;; A_s1
    card-d0-s1-v1 - card    ;; Q_s1
    card-d0-s1-v2 - card    ;; K_s1
    card-d0-s2-v0 - card    ;; A_s2
    card-d0-s2-v1 - card    ;; Q_s2
    card-d0-s2-v2 - card    ;; K_s2
    pile-0 - tableau
    pile-1 - tableau
    pile-2 - tableau
    deal-0 - deal
    deal-1 - deal
)

(:init
    ;; --- pile-0: K_s0 bottom, Q_s0 top -----------------------------------
    (on card-d0-s0-v2 pile-0)
    (on card-d0-s0-v1 card-d0-s0-v2)
    (clear card-d0-s0-v1)
    (in-play card-d0-s0-v1)
    (in-play card-d0-s0-v2)

    ;; --- pile-1: K_s1 bottom, Q_s1 top -----------------------------------
    (on card-d0-s1-v2 pile-1)
    (on card-d0-s1-v1 card-d0-s1-v2)
    (clear card-d0-s1-v1)
    (in-play card-d0-s1-v1)
    (in-play card-d0-s1-v2)

    ;; --- pile-2: K_s2 bottom, Q_s2 top -----------------------------------
    (on card-d0-s2-v2 pile-2)
    (on card-d0-s2-v1 card-d0-s2-v2)
    (clear card-d0-s2-v1)
    (in-play card-d0-s2-v1)
    (in-play card-d0-s2-v2)

    ;; --- deal-0 stack (bottom-up): deal-0, A_s2, A_s1, A_s0 (clear) ------
    (on card-d0-s2-v0 deal-0)
    (on card-d0-s1-v0 card-d0-s2-v0)
    (on card-d0-s0-v0 card-d0-s1-v0)
    (clear card-d0-s0-v0)

    ;; --- deal-1 sentinel: empty, already clear ---------------------------
    (clear deal-1)

    (current-deal deal-0)

    ;; --- CAN-CONTINUE-GROUP (same-suit consecutive runs) -----------------
    (CAN-CONTINUE-GROUP card-d0-s0-v0 card-d0-s0-v1)
    (CAN-CONTINUE-GROUP card-d0-s0-v1 card-d0-s0-v2)
    (CAN-CONTINUE-GROUP card-d0-s1-v0 card-d0-s1-v1)
    (CAN-CONTINUE-GROUP card-d0-s1-v1 card-d0-s1-v2)
    (CAN-CONTINUE-GROUP card-d0-s2-v0 card-d0-s2-v1)
    (CAN-CONTINUE-GROUP card-d0-s2-v1 card-d0-s2-v2)

    ;; --- CAN-BE-PLACED-ON: value v_n on any value v_(n+1) ----------------
    ;;     v0 (Ace) on v1 (Queen): 3 × 3 = 9
    (CAN-BE-PLACED-ON card-d0-s0-v0 card-d0-s0-v1)
    (CAN-BE-PLACED-ON card-d0-s0-v0 card-d0-s1-v1)
    (CAN-BE-PLACED-ON card-d0-s0-v0 card-d0-s2-v1)
    (CAN-BE-PLACED-ON card-d0-s1-v0 card-d0-s0-v1)
    (CAN-BE-PLACED-ON card-d0-s1-v0 card-d0-s1-v1)
    (CAN-BE-PLACED-ON card-d0-s1-v0 card-d0-s2-v1)
    (CAN-BE-PLACED-ON card-d0-s2-v0 card-d0-s0-v1)
    (CAN-BE-PLACED-ON card-d0-s2-v0 card-d0-s1-v1)
    (CAN-BE-PLACED-ON card-d0-s2-v0 card-d0-s2-v1)
    ;;     v1 (Queen) on v2 (King): 3 × 3 = 9
    (CAN-BE-PLACED-ON card-d0-s0-v1 card-d0-s0-v2)
    (CAN-BE-PLACED-ON card-d0-s0-v1 card-d0-s1-v2)
    (CAN-BE-PLACED-ON card-d0-s0-v1 card-d0-s2-v2)
    (CAN-BE-PLACED-ON card-d0-s1-v1 card-d0-s0-v2)
    (CAN-BE-PLACED-ON card-d0-s1-v1 card-d0-s1-v2)
    (CAN-BE-PLACED-ON card-d0-s1-v1 card-d0-s2-v2)
    (CAN-BE-PLACED-ON card-d0-s2-v1 card-d0-s0-v2)
    (CAN-BE-PLACED-ON card-d0-s2-v1 card-d0-s1-v2)
    (CAN-BE-PLACED-ON card-d0-s2-v1 card-d0-s2-v2)

    ;; --- IS-ACE / IS-KING ------------------------------------------------
    (IS-ACE card-d0-s0-v0)
    (IS-ACE card-d0-s1-v0)
    (IS-ACE card-d0-s2-v0)
    (IS-KING card-d0-s0-v2)
    (IS-KING card-d0-s1-v2)
    (IS-KING card-d0-s2-v2)

    ;; --- deal sequencing -------------------------------------------------
    (NEXT-DEAL deal-0 deal-1)

    ;; --- TO-DEAL: which pile each deal card goes to, and the card under it
    ;;     in the deal stack (used to keep `clear` valid after the card leaves)
    (TO-DEAL card-d0-s0-v0 pile-0 deal-0 card-d0-s1-v0)
    (TO-DEAL card-d0-s1-v0 pile-1 deal-0 card-d0-s2-v0)
    (TO-DEAL card-d0-s2-v0 pile-2 deal-0 deal-0)

    (= (total-cost) 0)
)

(:goal
    (and
        (clear pile-0)
        (clear pile-1)
        (clear pile-2)
        (clear deal-0)
        (on card-d0-s0-v0 discard)
        (on card-d0-s0-v1 discard)
        (on card-d0-s0-v2 discard)
        (on card-d0-s1-v0 discard)
        (on card-d0-s1-v1 discard)
        (on card-d0-s1-v2 discard)
        (on card-d0-s2-v0 discard)
        (on card-d0-s2-v1 discard)
        (on card-d0-s2-v2 discard)
    )
)

(:metric minimize (total-cost))
)
