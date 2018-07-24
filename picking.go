package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
	"strconv"
)

func main() {
	scores := readScores()
	teams, err := strconv.Atoi(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	players := os.Args[2:]
	if len(players) % teams > 0 {
		fmt.Printf("Jogadores sobrando: %v\n", len(players) % teams)
		return
	}
	picker := newPicker(scores, len(players) / teams, players)
	picker.pick(teams, nil)
	picker.print()
}

func readScores() map[string]float64 {
	scores := make(map[string]float64)
	r := bufio.NewReader(os.Stdin)
	for true {
		line, err := r.ReadString('\n')
		if err != nil {
			break
		}
		fields := strings.Split(strings.Trim(line, "\n"), " ")
		if fields == nil {
			log.Fatal("fields == nil")
		}
		f, err := strconv.ParseFloat(fields[2], 64)
		if err != nil {
			log.Fatal(err)
		}
		scores[fields[1]] = f
	}
	return scores
}

func newPicker(score map[string]float64, size int, players []string) picker {
	sort.Sort(byScore{players, score})
	return picker{score, size, players, 999999, nil}
}

type picker struct {
	score map[string]float64
	size int
	players []string
	bestDiff float64
	best [][]int
}

func (p *picker) pick(teams int, picked [][]int) {
	if teams == 0 {
		best := -999999.0
		worst := 999999.0
		for _, team := range picked {
			score := 0.0
			for _, player := range team {
				score += p.score[p.players[player]]
			}
			if score > best {
				best = score
			}
			if score < worst {
				worst = score
			}
		}
		diff := best - worst
		if diff < p.bestDiff {
			p.best = make([][]int, len(picked))
			for i := range picked {
				p.best[i] = make([]int, len(picked[i]))
				copy(p.best[i], picked[i])
			}
			p.bestDiff = diff
		}
		return
	}
	var all_picked []int
	for _, team := range picked {
		all_picked = append(all_picked, team...)
	}
	selection := newSelection(p.size, len(p.players), all_picked)
	for selection.next() {
		picked = append(picked, selection.selection)
		p.pick(teams - 1, picked)
		picked = picked[:len(picked) - 1]
	}
}

func (p *picker) print() {
	for _, team := range p.best {
		total := 0.0
		for _, player := range team {
			fmt.Printf("%v ", p.players[player])
			total += p.score[p.players[player]]
		}
		fmt.Printf("%v\n", total)
	}
}

type byScore struct {
	players []string
	score map[string]float64
}

func (b byScore) Len() int {
	return len(b.players)
}

func (b byScore) Swap(i, j int) {
	b.players[i], b.players[j] = b.players[j], b.players[i]
}

func (b byScore) Less(i, j int) bool {
	return b.score[b.players[i]] > b.score[b.players[j]]
}

func newSelection(size, max int, picked []int) *selection {
	s := make([]int, size)
	for i := range s {
		s[i] = -1
	}
	return &selection{s, max, newPicked(max, picked)}
}

type selection struct {
	selection []int
	max int
	picked *picked
}

func (s *selection) next() bool {
	if s.selection[0] == -1 {
		s.selection[0] = s.picked.next(-1)
		s.fill(1)
		return true
	}
	return s.nextPos(len(s.selection) - 1)
}

func (s *selection) fill(pos int) bool {
	for i := pos; i < len(s.selection); i++ {
		s.selection[i] = s.picked.next(s.selection[i - 1])
		if s.selection[i] == -1 {
			return false
		}
	}
	return true
}

func (s *selection) nextPos(pos int) bool {
	if pos == -1 {
		return false
	}
	s.selection[pos] = s.picked.next(s.selection[pos])
	if s.selection[pos] == -1 || !s.fill(pos + 1) {
		return s.nextPos(pos - 1)
	}
	return true
}

func newPicked(size int, pickedList []int) *picked {
	pickedMap := make([]bool, size)
	for _, p := range pickedList {
		pickedMap[p] = true
	}
	return &picked{pickedMap}
}

type picked struct {
	picked []bool
}

func (p *picked) next(pos int) int {
	pos += 1
	for pos < len(p.picked) && p.picked[pos] {
		pos += 1
	}
	if pos >= len(p.picked) {
		return -1
	}
	return pos
}
