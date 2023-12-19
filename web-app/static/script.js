function reroll() {
    // Redirect to the song route to fetch new recommendations
    window.location.href = "{{ url_for('song') }}";
}
