"use strict";

//<![CDATA[
function loadCSS(e, t, n) {
  "use strict";

  var i = window.document.createElement("link");
  var o = t || window.document.getElementsByTagName("script")[0];
  i.rel = "stylesheet";
  i.href = e;
  i.media = "only x";
  o.parentNode.insertBefore(i, o);
  setTimeout(function () {
    i.media = n || "all";
  });
}

loadCSS("//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.2/styles/sunburst.min.css");
hljs.initHighlightingOnLoad();
hljs.configure({
  useBR: false
});
$("div.code").each(function (e, t) {
  hljs.highlightBlock(t);
}); //]]>