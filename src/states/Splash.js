import Phaser from 'phaser'
import { centerGameObjects } from '../utils'

export default class extends Phaser.State {
  init () {}

  preload () {
    this.loaderBg = this.add.sprite(this.game.world.centerX, this.game.world.centerY, 'loaderBg')
    this.loaderBar = this.add.sprite(this.game.world.centerX, this.game.world.centerY, 'loaderBar')
    centerGameObjects([this.loaderBg, this.loaderBar])

    this.load.setPreloadSprite(this.loaderBar)
    //
    // load your assets
    //
    this.load.spritesheet('player', 'assets/images/player.png', 20, 26, 12, 0, 2);
    this.load.spritesheet('circlebot', 'assets/images/circlebot.png', 19, 19);
    this.load.spritesheet('wheelbot', 'assets/images/wheelbot.png', 16, 16);
    this.load.image('door', 'assets/images/door.png');

    this.load.image('tiles', 'assets/images/tiles.png');

    this.load.image('bg', 'assets/images/bg.png');
  }

  create () {
    this.state.start('Game', true, false, 1)
  }
}
