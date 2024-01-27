const toggleSwitch = document.getElementById('darkModeToggle');
		const currentTheme = localStorage.getItem('theme');
	
		if (currentTheme) {
		  document.documentElement.setAttribute('data-theme', currentTheme);
		  toggleSwitch.checked = currentTheme === 'dark';
		}
	
		function switchTheme() {
		  if (toggleSwitch.checked) {
			setTheme('dark');
		  } else {
			setTheme('light');
		  }
		}
	
		function setTheme(theme) {
		  document.documentElement.setAttribute('data-theme', theme);
		  localStorage.setItem('theme', theme);
		}
	
		toggleSwitch.addEventListener('change', switchTheme, false);