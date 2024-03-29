import pygame
import random
from Play_Screen.alien import Alien
from Play_Screen.alien_bullet import AlienBullet
from UI.all_enums import AlienPattern as AP
from UI.all_enums import CollisionsStates as CS
from Play_Screen.boss import Boss
from UI.all_enums import BossPattern as BP
from UI.all_enums import AlienColors as AC

class Horde:
    """A class to handle all alien methods and things"""
    def __init__(self, ai_game):
        """Initialize the horde"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.alien_pattern = ai_game.alien_pattern
        self.ship = ai_game.ship
        self.ai_game = ai_game
        self.boss = Boss(self, 1)
        self.boss_shell = pygame.sprite.GroupSingle()
        self.boss_shell.add(self.boss)

        self.aliens = pygame.sprite.Group()
        # for AP.THREEROWS only
        self.column1_aliens = pygame.sprite.Group()
        self.column2_aliens = pygame.sprite.Group()
        self.column3_aliens = pygame.sprite.Group()
        self.column4_aliens = pygame.sprite.Group()
        self.four_columns_group = [self.column1_aliens, self.column2_aliens, self.column3_aliens, self.column4_aliens]
        self.single_column_states_left = [CS.FIRSTCOLUMNLEFT, CS.FOURTHCOLUMNLEFT,
                                        CS.SECONDCOLUMNLEFT, CS.THIRDCOLUMNLEFT]
        self.single_column_states_right = [CS.FIRSTCOLUMNRIGHT, CS.FOURTHCOLUMNRIGHT,
                                        CS.SECONDCOLUMNRIGHT, CS.THIRDCOLUMNRIGHT]
        self.collision_column_list = [CS.FIRSTTWO, CS.TWOTHREE, CS.ONETHREE, CS.ONEFOUR, CS.TWOFOUR, CS.THREEFOUR]
        self.rows = [AP.TWOROWS, AP.THREEROWS, AP.FOURROWS, AP.BASIC]
        # Alien bullet group
        self.alien_bullets = pygame.sprite.Group()
    
    def _update_aliens(self):
        """
        Check if the fleet is at an edge, 
          then update the positions of all aliens in the fleet.
        """
        self.alien_pattern = self.ai_game.alien_pattern
        self._check_alien_ship_collisions_and_update()
        self._check_fleet_edges()
        self._check_aliens_bottom()
        self._check_bullet_collisions()

        # Fire the shooter aliens if needed.
        self._fire_shooter_aliens()

    def _check_bullet_collisions(self):
        """Check the alien projectile collisions with the ship (and shield with beam)"""
        if self.alien_pattern in [AP.THREEROWS, AP.BASIC, AP.TWOROWS, AP.FOURROWS]:
            if pygame.sprite.spritecollide(self.ship, self.alien_bullets, True):
                self.ai_game._ship_hit()
        elif self.alien_pattern == AP.BOSSROOM:
            if pygame.sprite.spritecollide(self.ship, self.boss.alien_bullets, True):
                if self.boss.rect.bottom >= 550:
                    self.boss.ydirection = -1
                    self.boss.rect.y -= 40
                self.ai_game._ship_hit()
            elif self.boss.beam_hitbox:
                if self.settings.warp_up and pygame.Rect.colliderect(self.ai_game.warp_shield.rect, self.boss.beam_rect):
                    self.ai_game._shield_hit(hits = 3)
                    self.boss.beam_rect.height = (self.ai_game.warp_shield.rect.top - self.boss.rect.bottom - 20)
                elif pygame.Rect.colliderect(self.ship.rect, self.boss.beam_rect):
                    self.boss.boss_pattern = random.choice([BP.SHOOTBASIC, BP.DARTTOHIT])
                    self.boss.ydirection = -1
                    self.ai_game._ship_hit()

    def _check_alien_ship_collisions_and_update(self):
        """Update, and then check alien-ship collisions"""
        if self.alien_pattern in self.rows:
            for group in self.four_columns_group:
                group.update()
                if pygame.sprite.spritecollideany(self.ship, group):
                    self.ai_game._ship_hit()
        elif self.alien_pattern == AP.BOSSROOM:
            self.boss.update()
            if pygame.sprite.spritecollide(self.ship, self.boss_shell, False):
                self.boss.ydirection = -1
                self.boss.rect.y -= 30
                self.ai_game._ship_hit()

    def _fire_shooter_aliens(self):
        """Have one alien shoot at any one time, earlier list address favored"""
        # Runs through every shooter alien address
        if self.alien_pattern in self.rows:
            if (len(self.alien_bullets) <= self.settings.alien_bullets_allowed):
                for address in self.shooter_alien_addresses:
                    for group in self.four_columns_group:
                        if (self._check_in_front(address, group) and 
                        self.alien_start_list[address] in group):
                            if self.shooter_alien_cooldowns[self.alien_start_list[address]] >= 50:
                                self.shooter_alien_cooldowns[self.alien_start_list[address]]= 0
                                new_bullet = AlienBullet(self, self.alien_start_list[address])
                                self.alien_bullets.add(new_bullet)
        for address in self.shooter_alien_addresses:
            self.shooter_alien_cooldowns[self.alien_start_list[address]] += 1
            #print(self.shooter_alien_cooldowns)
    
    def _update_alien_bullets(self):
        """Update alien bullets and get rid of out of bounds ones."""
        # Update their position
        self.alien_bullets.update()

        # If out of bounds, delete the bullet
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height - 35:
                self.alien_bullets.remove(bullet)

    def _check_in_front(self, alien, group):
        """Check before firing that no aliens in specified group are in front of the shooter"""
        if alien > self.number_aliens_x * 3 - 1: 
            return True
        elif (alien // self.number_aliens_x == 2 
                    and (self.alien_start_list[alien + self.number_aliens_x] in group)):
            return False
        elif alien // self.number_aliens_x == 1:
            for x in range(1, 3):
                if self.alien_start_list[alien + self.number_aliens_x * x] in group:
                    return False
        elif alien < self.number_aliens_x:
            for x in range(1, 4):
                if self.alien_start_list[alien + self.number_aliens_x * x] in group:
                    return False
        return True

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Make an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        self.shooters_made = 0
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        self.number_aliens_x = available_space_x // (2 * alien_width)
        # Ensures that even split rows can be divided evenly
        if self.alien_pattern in [AP.TWOROWS, AP.FOURROWS] and self.number_aliens_x % 2 != 0:
            self.number_aliens_x -= 1
            self.change_offset = True
        else: self.change_offset = False
        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                    (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the list of potential shooter aliens/addresses
        self.shooter_alien_addresses = []
        self.shooter_alien_cooldowns = {}
        self.time_since_shot = 0

        # Created here so each new alien in this mode can be appended
        self.alien_start_list = []

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(self.number_aliens_x):
                self._create_alien(alien_number, row_number)
        for x in range(random.randint(self.ai_game.stats.level, self.ai_game.stats.level + 2)):
            self._convert_normal_to_shooter(AC.RED)
        if self.ai_game.stats.level > 5:
            self._convert_normal_to_shooter(AC.PURPLE)

    def _convert_normal_to_shooter(self, color):
        selected = random.randint(0, self.number_aliens_x*4-1)
        self.alien_start_list[selected].change_color(color)
        self.shooters_made += 1
        self.shooter_alien_addresses.append(selected)
        self.shooter_alien_cooldowns[self.alien_start_list[selected]] = 0

    def _create_alien(self, alien_number, row_number):
        """Create a alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        if self.change_offset:
            offset = alien_width
        else: offset = 0
        alien.x = alien_width + offset + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        alien._generate_alien_address(alien_number, row_number)
        """if random.randint(1, self.number_aliens_x * 4) <= (self.ai_game.stats.level * 2) and self.shooters_made <= (self.ai_game.stats.level+1):
            alien.change_color(AC.RED)
            self.shooters_made += 1
            self.shooter_alien_addresses.append(alien_number + row_number * self.number_aliens_x)
            alien.shot_cooldown = 0
            self.shooter_alien_cooldowns[alien] = alien.shot_cooldown"""
        if self.alien_pattern in self.rows:
            number_rows = self.alien_pattern._value_[2]
            if alien_number < self.number_aliens_x // number_rows:
                self.column1_aliens.add(alien)
            elif alien_number < self.number_aliens_x // (number_rows / 2):
                self.column2_aliens.add(alien)
            elif alien_number < self.number_aliens_x // (number_rows / 3):
                self.column3_aliens.add(alien)
            else: self.column4_aliens.add(alien)
        self.alien_start_list.append(alien)

    def _check_fleet_edges(self):
        """Respond if aliens have reached an edge."""
        if self.alien_pattern in self.rows:
            for row_group in self.four_columns_group:
                for alien in row_group:
                    check = alien.check_edges()
                    if check in self.single_column_states_right or check in self.single_column_states_left:
                        self._single_column_actions(check)
                    elif check in self.collision_column_list:
                        self._colliding_columns_actions(check)

    def _single_column_actions(self, check):
        """Respond if a column hits the edge of the screen"""
        check_value = check._value_[0]
        self.settings.column_direction_list[check_value] *= -1
        self._drop_alien_group(self.four_columns_group[check_value])
        if check in self.single_column_states_left:
            for alien in self.four_columns_group[check_value]:
                alien.x += self.settings.alien_speed
                alien.rect.x = alien.x
        elif check in self.single_column_states_right:
            for alien in self.four_columns_group[check_value]:
                alien.x -= self.settings.alien_speed
                alien.rect.x = alien.x

    def _colliding_columns_actions(self, check):
        """Respond if columns collide"""
        for column in check._value_:
            self.settings.column_direction_list[column] *= -1
            self._drop_alien_group(self.four_columns_group[column])
            for alien in self.four_columns_group[column]:
                if column == check._value_[0]:
                    alien.x -= self.settings.alien_speed
                elif column == check._value_[1]:
                    alien.x += self.settings.alien_speed
                alien.rect.x = alien.x

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        if self.alien_pattern in self.rows:
            for group in self.four_columns_group:
                for alien in group:
                    if alien.rect.bottom >= screen_rect.bottom:
                        self.ai_game._ship_hit()
                        break

    def _drop_alien_group(self, group):
        """For more selective dropping of groups"""
        for alien in group:
            alien.rect.y += (self.settings.group_drop_speed / self.alien_pattern._value_[3])
