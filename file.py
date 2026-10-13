import math
import time
import tkinter as tk

WIDTH, HEIGHT = 960, 640
FLOOR = 550
GRAVITY = 900.0
BALL_R = 14

START_X, START_Y = 210.0, 476.0
HOOP_X, HOOP_Y = 760.0, 246.0
HALF_RIM = 35.0
BOARD_X, BOARD_TOP, BOARD_BOTTOM = 808.0, 148.0, 274.0

STEP = 1 / 120


class BasketballGame:
    def __init__(self, root):
        self.root = root
        self.closed = False
        self.keys = set()
        self.pending_releases = {}

        root.title("농구 슛 게임")
        root.resizable(False, False)

        self.canvas = tk.Canvas(
            root, width=WIDTH, height=HEIGHT,
            bg="#101b2b", highlightthickness=0
        )
        self.canvas.pack()

        self.restart()
        self.draw_background()

        root.bind("<KeyPress>", self.key_down)
        root.bind("<KeyRelease>", self.key_up)
        root.bind("<FocusOut>", self.focus_out)
        root.protocol("WM_DELETE_WINDOW", self.close)

        self.last_time = time.perf_counter()
        self.accumulator = 0.0
        self.canvas.focus_set()
        self.tick()

    def text(self, x, y, text, size=14, color="#e7eef7",
             anchor="center", tag="dynamic"):
        self.canvas.create_text(
            x, y, text=text, fill=color, anchor=anchor,
            font=("Malgun Gothic", size), tags=tag
        )

    def reset_ball(self):
        self.x, self.y = START_X, START_Y
        self.vx = self.vy = 0.0
        self.active = False
        self.scored = False
        self.charging = False
        self.power = 0.0
        self.age = 0.0
        self.finish_in = None

    def restart(self):
        self.angle = 55.0
        self.shots = self.made = self.streak = 0
        self.message = "스페이스바를 누르고 있다가 놓으면 슛!"
        self.message_color = "#dbe6f2"
        self.keys.clear()
        self.reset_ball()

    def velocity(self, power):
        speed = 380 + 720 * power
        angle = math.radians(self.angle)
        return speed * math.cos(angle), -speed * math.sin(angle)

    def key_down(self, event):
        key = event.keysym.lower()

        # 운영체제의 키 반복으로 발생하는 가짜 KeyRelease를 취소합니다.
        job = self.pending_releases.pop(key, None)
        if job is not None:
            self.root.after_cancel(job)

        if key in self.keys:
            return
        self.keys.add(key)

        if key == "escape":
            self.close()
        elif key == "r":
            self.restart()
        elif key == "space" and not self.active:
            self.charging = True
            self.power = 0.0

    def key_up(self, event):
        key = event.keysym.lower()
        job = self.pending_releases.pop(key, None)
        if job is not None:
            self.root.after_cancel(job)

        self.pending_releases[key] = self.root.after(
            20, lambda: self.release(key)
        )

    def release(self, key):
        self.pending_releases.pop(key, None)
        self.keys.discard(key)

        if key == "space" and self.charging and not self.active:
            self.charging = False
            self.vx, self.vy = self.velocity(self.power)
            self.active = True
            self.shots += 1
            self.message = "슛!"
            self.message_color = "#dbe6f2"

    def focus_out(self, event):
        self.keys.clear()
        self.charging = False
        self.power = 0.0

        for job in self.pending_releases.values():
            self.root.after_cancel(job)
        self.pending_releases.clear()

    def close(self):
        self.closed = True
        self.root.destroy()

    def draw_background(self):
        c = self.canvas

        c.create_rectangle(
            0, 100, WIDTH, FLOOR, fill="#18283e", outline=""
        )
        for y in (150, 195, 240):
            c.create_line(30, y, 930, y, fill="#24394f", width=2)

        c.create_rectangle(
            0, FLOOR, WIDTH, HEIGHT, fill="#b8773f", outline=""
        )
        for x in range(0, WIDTH, 80):
            c.create_line(x, FLOOR, x - 32, HEIGHT, fill="#966032")

        c.create_line(
            0, FLOOR, WIDTH, FLOOR, fill="#efd0a0", width=3
        )
        c.create_oval(
            435, 566, 890, 730, outline="#f4d3a1", width=3
        )

        # 골대 지지대와 백보드
        c.create_line(
            833, 196, 867, 196, 867, FLOOR,
            fill="#536479", width=12
        )
        c.create_rectangle(
            BOARD_X, BOARD_TOP, BOARD_X + 10, BOARD_BOTTOM,
            fill="#c4dced", outline="#ffffff", width=2
        )

        # 그물
        for i in range(7):
            x = HOOP_X - HALF_RIM + 2 * HALF_RIM * i / 6
            c.create_line(
                x, HOOP_Y + 3,
                HOOP_X + (x - HOOP_X) * 0.58, HOOP_Y + 56,
                fill="#c4d6e6", width=2
            )
        for i in range(1, 4):
            y = HOOP_Y + i * 14
            half = HALF_RIM * (1 - 0.42 * i / 4)
            c.create_line(
                HOOP_X - half, y, HOOP_X + half, y,
                fill="#a7bed1"
            )

        # 간단한 선수
        c.create_oval(
            151, 441, 179, 469, fill="#f5bc82", outline=""
        )
        c.create_line(165, 477, 165, 505, fill="#60c9eb", width=22)
        c.create_line(
            165, 482, 188, 489, 204, 481,
            fill="#f5bc82", width=9
        )
        c.create_line(161, 506, 150, 540, fill="#cbd9ec", width=9)
        c.create_line(171, 506, 187, 540, fill="#cbd9ec", width=9)

        self.text(
            30, 35, "BASKETBALL", 24,
            "#ffffff", "w", "static"
        )
        self.text(
            30, 70, "KEYBOARD SHOOTING GAME", 10,
            "#86a2bd", "w", "static"
        )
        self.text(
            480, 614,
            "방향키: 각도  |  SPACE: 힘 모으기 → 놓아서 슛  "
            "|  R: 초기화  |  ESC: 종료",
            12, "#fff2dc", tag="static"
        )

    def reflect(self, nx, ny, restitution):
        toward = self.vx * nx + self.vy * ny
        if toward < 0:
            self.vx -= (1 + restitution) * toward * nx
            self.vy -= (1 + restitution) * toward * ny

    def collide_rim(self, rim_x):
        dx, dy = self.x - rim_x, self.y - HOOP_Y
        distance = math.hypot(dx, dy)
        limit = BALL_R + 4

        if distance < limit:
            if distance > 0.00001:
                nx, ny = dx / distance, dy / distance
            else:
                nx, ny = 0, -1

            self.x = rim_x + nx * limit
            self.y = HOOP_Y + ny * limit
            self.reflect(nx, ny, 0.62)

    def collide_board(self):
        nearest_x = min(max(self.x, BOARD_X), BOARD_X + 10)
        nearest_y = min(max(self.y, BOARD_TOP), BOARD_BOTTOM)
        dx, dy = self.x - nearest_x, self.y - nearest_y
        distance = math.hypot(dx, dy)

        if distance < BALL_R:
            if distance > 0.00001:
                nx, ny = dx / distance, dy / distance
            else:
                nx, ny = (-1, 0) if self.vx >= 0 else (1, 0)

            overlap = BALL_R - distance + 0.1
            self.x += nx * overlap
            self.y += ny * overlap
            self.reflect(nx, ny, 0.7)

    def end_shot(self):
        if not self.scored:
            self.streak = 0
            self.message = "아쉽네요! 각도와 힘을 조절해 보세요."
            self.message_color = "#ffce90"
        self.reset_ball()

    def update(self, dt):
        if not self.active:
            higher = bool({"left", "up"} & self.keys)
            lower = bool({"right", "down"} & self.keys)
            direction = int(higher) - int(lower)
            self.angle = max(
                30, min(80, self.angle + direction * 38 * dt)
            )

            if self.charging:
                self.power = min(1, self.power + dt / 1.2)
            return

        self.age += dt
        if self.finish_in is not None:
            self.finish_in -= dt
            if self.finish_in <= 0:
                self.end_shot()
                return

        old_x, old_y = self.x, self.y
        self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # 내려오는 공이 골대 내부를 통과한 경우에만 득점합니다.
        if not self.scored and self.vy > 0 and old_y < HOOP_Y <= self.y:
            fraction = (HOOP_Y - old_y) / (self.y - old_y)
            crossing_x = old_x + (self.x - old_x) * fraction
            clearance = HALF_RIM - BALL_R - 3

            if abs(crossing_x - HOOP_X) <= clearance:
                self.scored = True
                self.made += 1
                self.streak += 1
                self.finish_in = 0.9
                self.message = f"골! +2점  |  {self.streak}연속 성공"
                self.message_color = "#70efbd"

        self.collide_board()
        self.collide_rim(HOOP_X - HALF_RIM)
        self.collide_rim(HOOP_X + HALF_RIM)

        if self.y + BALL_R >= FLOOR:
            self.y = FLOOR - BALL_R
            if self.vy > 0:
                self.vy *= -0.38
                self.vx *= 0.72
            if self.finish_in is None:
                self.finish_in = 0.7

        if self.x < -80 or self.x > WIDTH + 80 or self.age > 5:
            self.end_shot()

    def draw(self):
        c = self.canvas
        c.delete("dynamic")

        accuracy = round(100 * self.made / self.shots) if self.shots else 0
        self.text(
            935, 35,
            f"{self.made * 2}점    {self.made}/{self.shots} 성공"
            f"    성공률 {accuracy}%",
            17, "#ffffff", "e"
        )
        self.text(
            935, 72,
            f"각도 {self.angle:.0f}°    파워 {self.power * 100:.0f}%",
            12, "#93c8eb", "e"
        )
        self.text(
            480, 125, self.message, 16, self.message_color
        )

        self.text(30, 377, "POWER", 10, "#bcd3e8", "w")
        c.create_rectangle(
            30, 399, 245, 419,
            fill="#0e1928", outline="#43617b", tags="dynamic"
        )
        if self.power > 0:
            color = "#69dfb6" if self.power < 0.85 else "#ffbc66"
            c.create_rectangle(
                32, 401, 32 + 211 * self.power, 417,
                fill=color, outline="", tags="dynamic"
            )

        # 짧은 예상 궤적
        if not self.active:
            preview_power = self.power if self.charging else 0.55
            vx, vy = self.velocity(preview_power)
            for i in range(1, 13):
                t = i * 0.055
                x = START_X + vx * t
                y = START_Y + vy * t + 0.5 * GRAVITY * t * t
                if y > FLOOR - BALL_R:
                    break
                c.create_oval(
                    x - 2, y - 2, x + 2, y + 2,
                    fill="#729cba", outline="", tags="dynamic"
                )

        x, y = self.x, self.y
        shadow = max(5, 16 - abs(FLOOR - y) * 0.016)
        c.create_oval(
            x - shadow, FLOOR - 5, x + shadow, FLOOR + 3,
            fill="#745030", outline="", tags="dynamic"
        )
        c.create_oval(
            x - BALL_R, y - BALL_R, x + BALL_R, y + BALL_R,
            fill="#f58a2d", outline="#422a1c",
            width=2, tags="dynamic"
        )
        c.create_line(
            x - BALL_R + 2, y, x + BALL_R - 2, y,
            fill="#593322", width=2, tags="dynamic"
        )
        c.create_arc(
            x - 6, y - BALL_R + 1, x + 6, y + BALL_R - 1,
            start=90, extent=180, style="arc",
            outline="#593322", width=2, tags="dynamic"
        )

        c.create_oval(
            HOOP_X - HALF_RIM, HOOP_Y - 5,
            HOOP_X + HALF_RIM, HOOP_Y + 5,
            outline="#ff8141", width=5, tags="dynamic"
        )

    def tick(self):
        if self.closed:
            return

        now = time.perf_counter()
        self.accumulator += min(now - self.last_time, 0.05)
        self.last_time = now

        while self.accumulator >= STEP:
            self.update(STEP)
            self.accumulator -= STEP

        self.draw()
        self.root.after(16, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    BasketballGame(root)
    root.mainloop()
