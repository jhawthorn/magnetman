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
    game.renderer.renderSession.roundPixels = true;
    game.stage.smoothed = false;

    game.physics.startSystem(Phaser.Physics.ARCADE);
    game.physics.arcade.gravity.y = 300;
    game.physics.arcade.setBoundsToWorld();

    this.map = game.add.tilemap('map1');
    this.map.addTilesetImage('magnoman', 'tiles');
    this.map.setCollisionBetween(0,80);
    this.layer = this.map.createLayer(0);
    this.layer.resizeWorld();

    this.background = game.add.tileSprite(0, 0, game.world.width, game.world.height, 'bg');
    game.world.sendToBack(this.background);


    this.player = new Player({
      game: this.game,
      x: this.world.centerY,
      y: this.world.centerY,
      map: this.map
    });

    this.game.add.existing(this.player);
    this.game.camera.follow(this.player, Phaser.Camera.FOLLOW_PLATFORMER);
  }

  update() {
    game.physics.arcade.collide(this.player, this.layer);
  }

  render () {
    game.debug.text(game.time.fps || '--', 2, 14, "#00ff00");
    //game.debug.body(this.player);
    game.debug.bodyInfo(this.player, 32, 20);
  }
}
