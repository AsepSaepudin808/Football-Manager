from odoo import models, fields, api

class FootballClub(models.Model):
    _name = 'football.club'
    _description = 'Football Club'

    name = fields.Char(string='Club Name', required=True)
    city = fields.Char(string='City', required=True)
    _sql_constraints = [
        ('unique_club', 'unique(name, city)', 'Club name and city must be unique.')
    ]

class FootballMatch(models.Model):
    _name = 'football.match'
    _description = 'Football Match'

    club1_id = fields.Many2one('football.club', string='Club 1', required=True)
    club2_id = fields.Many2one('football.club', string='Club 2', required=True)
    score1 = fields.Integer(string='Score 1', required=True)
    score2 = fields.Integer(string='Score 2', required=True)
    match_date = fields.Date(string='Match Date', required=True)
    _sql_constraints = [
        ('unique_match', 'unique(club1_id, club2_id, match_date)', 'Match must be unique.')
    ]

    @api.model
    def create(self, vals):
        record = super(FootballMatch, self).create(vals)
        self.env['football.league.standing'].update_standings()
        return record

class FootballLeagueStanding(models.Model):
    _name = 'football.league.standing'
    _description = 'Football League Standing'

    club_id = fields.Many2one('football.club', string='Klub', required=True)
    played = fields.Integer(string='Ma', compute='_compute_standings', store=True)
    won = fields.Integer(string='Me', compute='_compute_standings', store=True)
    draw = fields.Integer(string='S', compute='_compute_standings', store=True)
    lost = fields.Integer(string='K', compute='_compute_standings', store=True)
    goals_for = fields.Integer(string='GM', compute='_compute_standings', store=True)
    goals_against = fields.Integer(string='GK', compute='_compute_standings', store=True)
    points = fields.Integer(string='Point', compute='_compute_standings', store=True)


    @api.depends('club_id')
    def _compute_standings(self):
        for record in self:
            matches = self.env['football.match'].search(['|', ('club1_id', '=', record.club_id.id), ('club2_id', '=', record.club_id.id)])
            played = len(matches)
            won, draw, lost, goals_for, goals_against, points = 0, 0, 0, 0, 0, 0
            for match in matches:
                if match.club1_id == record.club_id:
                    goals_for += match.score1
                    goals_against += match.score2
                    if match.score1 > match.score2:
                        won += 1
                        points += 3
                    elif match.score1 == match.score2:
                        draw += 1
                        points += 1
                    else:
                        lost += 1
                else:
                    goals_for += match.score2
                    goals_against += match.score1
                    if match.score2 > match.score1:
                        won += 1
                        points += 3
                    elif match.score2 == match.score1:
                        draw += 1
                        points += 1
                    else:
                        lost += 1
            record.played = played
            record.won = won
            record.draw = draw
            record.lost = lost
            record.goals_for = goals_for
            record.goals_against = goals_against
            record.points = points

    @api.model
    def update_standings(self):
        self.env['football.league.standing'].search([]).unlink()
        clubs = self.env['football.club'].search([])
        for club in clubs:
            self.create({'club_id': club.id})


class FootballMatchTemp(models.TransientModel):
    _name = 'football.match.temp'
    _description = 'Temporary Football Match'

    wizard_id = fields.Many2one('football.match.wizard', string='Wizard Reference', required=False, ondelete='cascade')
    club1_id = fields.Many2one('football.club', string='Club 1', required=True)
    score1 = fields.Integer(string='Score 1', required=True)
    club2_id = fields.Many2one('football.club', string='Club 2', required=True)
    score2 = fields.Integer(string='Score 2', required=True)

class FootballMatchWizard(models.TransientModel):
    _name = 'football.match.wizard'
    _description = 'Football Match Wizard'

    match_ids = fields.One2many('football.match.temp', 'wizard_id', string='Matches')

    def action_save_matches(self):
        for match in self.match_ids:
            self.env['football.match'].create({
                'club1_id': match.club1_id.id,
                'score1': match.score1,
                'club2_id': match.club2_id.id,
                'score2': match.score2,
                'match_date': fields.Date.today()
            })
        return {'type': 'ir.actions.act_window_close'}