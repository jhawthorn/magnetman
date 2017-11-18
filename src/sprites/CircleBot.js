import Phaser from 'phaser'

export default class extends Phaser.Sprite {
  constructor ({ game, x, y, map }) {
    super(game, x, y, 'circlebot');

    game.physics.enable(this, Phaser.Physics.ARCADE);
    this.body.allowGravity = false;
    this.body.immovable = true;
    this.body.setSize(9, 9, 7, 7);

    this.animations.add('fly', [1,2], 5, true);
    this.animations.play('fly');
  }
}
