#!/bin/bash
echo '<html><head>
<meta http-equiv="content-type" content="text/html; charset=windows-1250"></head><body vlink="#006600" link="#009900" bgcolor="black">
<font color="lightGreen">
<pre>' > change.html
cat CHANGELOG >> change.html
echo '
</font>
</body></html></font>
</body></html>
' >> change.html
