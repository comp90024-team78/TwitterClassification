#!/bin/bash
curl "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary" \
-G \
--data-urlencode 'start_key=["'$1'",'$2']' \
--data-urlencode 'end_key=["'$1'",'$3']' \
--data-urlencode 'reduce=false' \
--data-urlencode 'include_docs=true' \
--user "readonly:ween7ighai9gahR6" \
