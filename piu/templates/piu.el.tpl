;;; piu.el --- interface to paste.in.ua
;;; -*- mode: emacs-lisp -*-

;;; Copyright (c) 2010 Alexander Solovyov under new BSD License

;;; Author: Alexander Solovyov
;;; Version: 1.0
;;; URL: http://paste.in.ua/piu.el

;;; Commentary:
;;;
;;; Add autoload to your configuration file:
;;;
;;;    (autoload 'piu "piu" "paste buffer or region" t)
;;;
;;; And then use it like "M-x piu" or add a shortcut:
;;;
;;;    (global-set-key (kbd "C-x p") 'piu)
;;;
;;; Executing this will result in pasted region if there was any (depends on
;;; transient-mark-mode) or a whole buffer.
;;;
;;; In either case url of pasted text is left on the kill ring, the paste buffer
;;; and (probably) copied to system buffer.
;;;
;;; Code:

(defvar piu-url "http://paste.in.ua/"
  "Url to paste.in.ua or compatible service.")

(defvar piu-types
  '((nxml-mode . "xml")
    (emacs-lisp-mode . "common-lisp")
    (c++-mode . "cpp")
    (conf-windows-mode . "ini")
    (conf-unix-mode . "ini")
    (cs-mode . "csharp")
    (js2-mode . "js")))

;;;###autoload
(defun piu ()
  "Paste either buffer or region if active."
  (interactive)
  (let* ((region (if (use-region-p) (cons (region-beginning) (region-end))
                  (cons (point-min) (point-max))))
         (url-request-method "POST")
         (url-request-extra-headers
          '(("Content-Type" . "application/x-www-form-urlencoded")))
         (url-request-data
          (format "lexer=%s&data=%s"
                  (url-hexify-string
                   (or (assoc-default major-mode piu-types)
                       (replace-regexp-in-string
                        "-" "" (substring (symbol-name major-mode) 0 -5))))
                  (url-hexify-string
                   (buffer-substring-no-properties (car region) (cdr region))))))
    (url-retrieve piu-url
                  (lambda (arg)
                    (cond
                     ((equal :error (car arg))
                      (signal 'piu-error (cdr arg)))
                     ((equal :redirect (car arg))
                      (with-temp-buffer
                        (insert (cadr arg))
                        (clipboard-kill-ring-save (point-min) (point-max))
                        (message "%s, copied to clipboard"
                                 (buffer-substring-no-properties (point-min) (point-max))))))))))

(provide 'piu)
;;; piu.el ends here
