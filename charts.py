import streamlit as st
import plotly.graph_objects as go


def show_mood_chart(sessions: list, nickname: str) -> None:
    """
    Renders a clear, labelled mood trend chart using Plotly.
    Uses session numbers on x-axis instead of dates to avoid
    collapsing when multiple sessions happen on the same day.
    """

    if len(sessions) < 2:
        st.info(
            f"👋 Welcome, **{nickname.capitalize()}**! "
            "Your progress chart will appear here from your second session onwards. "
            "Complete this session to start tracking your journey."
        )
        return

    # ── Build data ────────────────────────────────────────────────────────────
    # X axis — session numbers like Session 1, Session 2 etc.
    # Much cleaner than dates when sessions happen same day during testing
    session_labels = [f"Session {i+1}" for i in range(len(sessions))]

    mood_scores   = [s["emotional_state"] for s in sessions]
    stress_scores = [s["stress_level"] for s in sessions]
    sleep_scores  = [s["sleep_hours"] for s in sessions]

    # Hover text shows the actual date for context
    dates = [s["date"] for s in sessions]

    # ── Build Plotly figure ───────────────────────────────────────────────────
    fig = go.Figure()

    # Mood line — teal
    fig.add_trace(go.Scatter(
        x=session_labels,
        y=mood_scores,
        mode="lines+markers",
        name="Mood (1-10)",
        line=dict(color="#1D9E75", width=2.5),
        marker=dict(size=8, color="#1D9E75"),
        hovertemplate="<b>Mood:</b> %{y}/10<br><b>Date:</b> " +
                      "<br>".join(dates) + "<extra></extra>"
    ))

    # Stress line — coral/red
    # NOTE: High stress = bad. Chart shows it directly (no inversion).
    # Downward trend on this line = improvement. Label makes this clear.
    fig.add_trace(go.Scatter(
        x=session_labels,
        y=stress_scores,
        mode="lines+markers",
        name="Stress (1-10, lower is better)",
        line=dict(color="#D85A30", width=2.5),
        marker=dict(size=8, color="#D85A30"),
        hovertemplate="<b>Stress:</b> %{y}/10<extra></extra>"
    ))

    # Sleep line — purple
    fig.add_trace(go.Scatter(
        x=session_labels,
        y=sleep_scores,
        mode="lines+markers",
        name="Sleep (hours)",
        line=dict(color="#7F77DD", width=2.5),
        marker=dict(size=8, color="#7F77DD"),
        hovertemplate="<b>Sleep:</b> %{y} hrs<extra></extra>"
    ))

    # ── Layout ────────────────────────────────────────────────────────────────
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8888aa"),
        xaxis=dict(
            title="Sessions",
            showgrid=False,
            tickfont=dict(size=12, color="#8888aa"),
            linecolor="rgba(127,119,221,0.2)",
        ),
        yaxis=dict(
            title="Score",
            range=[0, 12],
            showgrid=True,
            gridcolor="rgba(127,119,221,0.1)",
            tickvals=[0, 2, 4, 6, 8, 10, 12],
            tickfont=dict(size=12, color="#8888aa"),
            linecolor="rgba(127,119,221,0.2)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color="#8888aa"),
            bgcolor="rgba(0,0,0,0)"
        ),
        hovermode="x unified",
        height=360,
    )

    # ── Render ────────────────────────────────────────────────────────────────
    st.markdown("### 📈 Your Wellbeing Journey")
    st.caption(
        f"{len(sessions)} sessions recorded · "
        f"Mood ↑ good · Stress ↓ good · Sleep ↑ good"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Summary metric cards ──────────────────────────────────────────────────
    first  = sessions[0]
    latest = sessions[-1]

    mood_change   = latest["emotional_state"] - first["emotional_state"]
    stress_change = latest["stress_level"]    - first["stress_level"]
    sleep_change  = latest["sleep_hours"]     - first["sleep_hours"]

    col1, col2, col3 = st.columns(3)

    with col1:
        # Mood: increase = good (default green for positive delta)
        st.metric(
            label="Mood",
            value=f"{latest['emotional_state']}/10",
            delta=f"{mood_change:+} since session 1"
            # default delta_color: green=positive, red=negative ✓ correct for mood
        )

    with col2:
        # Stress: decrease = good so we use delta_color="inverse"
        # inverse means: negative delta = green, positive delta = red
        st.metric(
            label="Stress",
            value=f"{latest['stress_level']}/10",
            delta=f"{stress_change:+} since session 1",
            delta_color="inverse"
            # Now: stress dropped by 1 → shows green ✓
            # stress went up by 2 → shows red ✓
        )

    with col3:
        # Sleep: increase = good (default)
        st.metric(
            label="Sleep",
            value=f"{latest['sleep_hours']} hrs",
            delta=f"{sleep_change:+} hrs since session 1"
        )

    # ── Motivational message ──────────────────────────────────────────────────
    st.divider()
    if mood_change > 0 and stress_change <= 0:
        st.success(
            "🌱 Your mood is improving and stress is coming down. "
            "The support plan is working — keep going."
        )
    elif mood_change < 0 or stress_change > 3:
        st.warning(
            "💙 Things seem harder than when you started. "
            "Consider revisiting your action plan or speaking to someone you trust."
        )
    else:
        st.info(
            "📊 Your journey is being tracked. "
            "Consistency is key — check in regularly to see your progress build."
        )