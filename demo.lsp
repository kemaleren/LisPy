(defun fact (x)
  (cond ((= x 1) 1)
        (T (* x (fact (- x 1))))))

(fact 1)
(fact 10)

(defun fib (n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        ((= n 2) 1)
        (T (+ (fib (- n 1))
              (fib (- n 2))))))

(fib 0)
(fib 1)
(fib 2)
(fib 3)
(fib 10)

(defun length (list)
  (cond ((null list) 0)
        (T (+ 1 (length (cdr list))))))

(length ())
(length (quote (a b c)))
(length . ((quote . ((a . (b . (c . NIL))) . NIL)) . NIL))


(cons 1 (quote (2 3)))

(defun push (list elt)
  (cond ((null list) (cons elt ()))
        (T (cons (car list)
                 (push (cdr list) elt)))))

(push (quote (1 2)) 3)


