function popSessionValues() {
    var prev_player_id = "{{ session['prev_player_id'] }}";
    if (prev_player_id != null) {
        $("#playerId").val(prev_player_id);
    }

    var prev_player_name = "{{ session['prev_player_name'] }}";
    if (prev_player_name != null) {
        $("#playerName").val(prev_player_name);
    }

    var prev_year = "{{ session['prev_year'] }}";
    if (prev_year != null) {
        if (prev_year != 0) {
            $("#year_select").val(prev_year).toInt();
        } else {
            $("#year_select").val("All");
        }
    }

    var prev_phase = "{{ session['prev_phase'] }}";
    if (prev_phase != null) {
        if (prev_phase != "0") {
            $("#phase_select").val(prev_phase);
        } else {
            $("#phase_select").val("All");
        }
    }

    var prev_week = "{{ session['prev_week'] }}";
    if (prev_week != null) {
        if (prev_week != 0) {
            $("#week_select").val(prev_week);
        } else {
            $("#week_select").val("All");
        }
    }
}
