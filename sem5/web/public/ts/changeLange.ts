export const listenLangChange = () => {
  const select = document.getElementById('lang') as HTMLSelectElement;

  const urlParams = new URLSearchParams(window.location.search);
  const currentLang = urlParams.get('lang') || 'ru'; 
  select.value = currentLang;

  select.addEventListener('change', () => {
    const url = new URL(window.location.href);
    url.searchParams.set('lang', select.value);

    window.location.href = url.toString();
  });
}