(function(){var selectedTheme=checkColorTheme();if(selectedTheme)document.getElementsByTagName("html")[0].setAttribute('data-theme',selectedTheme);function checkColorTheme(){return(localStorage.getItem('colorTheme')!==null)?localStorage.getItem('colorTheme'):false;};}());