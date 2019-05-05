echo Content-Type: text/html
echo
echo "<html><body>"
echo "<form enctype=\"multipart/form-data\" action=\"\" method=\"post\">"
echo "<p>Local File: <input name=\"userfile\" type=\"file\">"
echo "<input type=\"submit\" value=\"Send\">"
echo "</form><br><br><br>"
echo "<hr>"
dd count=$CONTENT_LENGTH bs=1 of=/tmp/test
lineas=`cat /tmp/test | wc -l`
lineas2=`expr $lineas - 4`
lineas3=`expr $lineas2 - 1`
tail -$lineas2 /tmp/test > /tmp/test2
head -$lineas3 /tmp/test2 > /tmp/upload
echo "<pre>"
cat /tmp/upload
echo "</pre>"

