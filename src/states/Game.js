/* globals __DEV__ */
import Phaser from 'phaser'
import Player from '../sprites/Player'

export default class extends Phaser.State {
  init () {
    this.stage.backgroundColor = '#292634';
    //this.game.scale.windowConstraints.bottom = "visual";
    //this.game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
  }

  preload () {
    game.time.advancedTiming = true;
  }

  create () {
    //this.map = game.add.tilemap('map');
    //var layer = this.map.createLayer(0);
    //layer.resizeWorld();
    //game.world.setBounds(0, 0, 600, 600);

    //this.map.createLayer(1);

    const bannerText = 'MagneMan';
    let banner = this.add.text(this.world.centerX, 80, bannerText);
    banner.font = 'Bangers';
    banner.padding.set(10, 16);
    banner.fontSize = 40;
    banner.fill = '#77BFA3';
    banner.smoothed = false;
    banner.anchor.setTo(0.5);

    this.player = new Player({
      game: this.game,
      x: this.world.centerY,
      y: this.world.centerY
    });

    this.game.add.existing(this.player);
    this.game.camera.follow(this.player, Phaser.Camera.FOLLOW_LOCKON);
  }

  render () {
    game.debug.text(game.time.fps || '--', 2, 14, "#00ff00");
  }
}
