import Phaser from 'phaser'

export default class extends Phaser.Sprite {
  constructor ({ game, x, y, map }) {
    super(game, x, y, 'wheelbot');

    game.physics.enable(this, Phaser.Physics.ARCADE);
    this.body.allowGravity = false;
    this.body.immovable = true;

    this.body.velocity.x = 100;
    this.body.bounce.x = 1;
  }
}
