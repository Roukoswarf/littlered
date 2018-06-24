var navs = document.getElementsByName('expandnav');
var loginusername = document.getElementById('id_username');
var checked;
for ( x in navs ) {
	navs[x].onclick = function() {
		if(checked == this){
			this.checked = false;
			checked = null;
		} else {
			checked = this;
			if (this.id == 'login') {
				loginusername.focus();
			}
		}
	};
}
