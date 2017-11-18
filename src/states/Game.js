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

    this.background = game.add.tileSprite(0, 0, game.width * 2, game.height * 2, 'bg');
    this.background.fixedToCamera = true;
    game.world.sendToBack(this.background);

    this.map.objects.objects.forEach((object) => {
      if(object.type == "player") {
        this.player = new Player({
          game: this.game,
          x: object.x,
          y: object.y,
          map: this.map
        });
      }
    });

    this.game.add.existing(this.player);
    game.world.bringToTop(this.layer);

    this.game.camera.follow(this.player, Phaser.Camera.FOLLOW_PLATFORMER);
  }

  update() {
    game.physics.arcade.collide(this.player, this.layer);

    this.background.anchor.x = (this.game.camera.x / this.background.width / 2) % 0.5;
    this.background.anchor.y = (this.game.camera.y / this.background.height / 2) % 0.5;
  }

  render () {
    game.debug.text(game.time.fps || '--', 2, 14, "#00ff00");
    //game.debug.body(this.player);
    game.debug.bodyInfo(this.player, 32, 20);
  }
}
